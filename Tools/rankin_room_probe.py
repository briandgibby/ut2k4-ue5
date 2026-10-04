"""Fixed Flak atrium geometry spike using Blender's native OBJ/FBX tools."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


OBJ_MIN = (768.0, -512.0, -2720.0)
OBJ_MAX = (1920.0, 1024.0, -1376.0)


def bounds(obj):
    corners = [obj.matrix_world @ vertex.co for vertex in obj.data.vertices]
    return (
        [min(corner[axis] for corner in corners) for axis in range(3)],
        [max(corner[axis] for corner in corners) for axis in range(3)],
    )


def snapshot(objects):
    result = {}
    for obj in objects:
        mesh = obj.data
        uv_layer = mesh.uv_layers.active
        corners = [
            tuple(obj.matrix_world @ mesh.vertices[loop.vertex_index].co)
            + tuple(uv_layer.data[index].uv)
            for index, loop in enumerate(mesh.loops)
        ]
        lower, upper = bounds(obj)
        materials = [mesh.materials[face.material_index].name for face in mesh.polygons]
        result[obj.name] = {
            "vertices": len(mesh.vertices),
            "faces": len(mesh.polygons),
            "uv_corners": len(corners),
            "bounds_min_source_units": lower,
            "bounds_max_source_units": upper,
            "material_slots": [material.name for material in mesh.materials],
            "material_face_coverage": dict(Counter(materials)),
            "uv_min": [min(corner[axis] for corner in corners) for axis in (3, 4)],
            "uv_max": [max(corner[axis] for corner in corners) for axis in (3, 4)],
            "_corners": corners,
            "_face_materials": materials,
            "_face_material_indices": [face.material_index for face in mesh.polygons],
        }
    return result


def verify(expected, actual):
    passed = set(expected) == set(actual)
    position_error = 0.0
    uv_error = 0.0
    material_labels_preserved = True
    material_label_changes = {}
    material_slot_counts_match = True
    polygon_material_indices_match = True
    alias_targets = {}
    for name in set(expected) & set(actual):
        before, after = expected[name], actual[name]
        passed &= all(before[key] == after[key] for key in ("vertices", "faces", "uv_corners"))
        material_slot_counts_match &= len(before["material_slots"]) == len(after["material_slots"])
        polygon_material_indices_match &= before["_face_material_indices"] == after["_face_material_indices"]
        material_labels_preserved &= before["_face_materials"] == after["_face_materials"]
        for reference, measured in zip(before["material_slots"], after["material_slots"]):
            alias_targets.setdefault(measured, set()).add(reference)
            if reference != measured:
                material_label_changes[reference] = measured
        for reference, measured in zip(before["_corners"], after["_corners"]):
            position_error = max(position_error, *(abs(reference[axis] - measured[axis]) for axis in range(3)))
            uv_error = max(uv_error, *(abs(reference[axis] - measured[axis]) for axis in (3, 4)))
    collisions = {name: sorted(originals) for name, originals in alias_targets.items() if len(originals) > 1}
    passed &= position_error <= 0.001 and uv_error <= 0.000001 and material_slot_counts_match and polygon_material_indices_match and not collisions
    return {"passed": bool(passed), "objects": len(actual), "max_position_error_source_units": position_error, "max_uv_error": uv_error, "material_slot_counts_match": bool(material_slot_counts_match), "polygon_material_indices_match": bool(polygon_material_indices_match), "ambiguous_material_alias_collisions": collisions, "material_labels_preserved": bool(material_labels_preserved), "stock_material_label_changes": material_label_changes}


def main():
    import bmesh
    import bpy
    from mathutils import Matrix, Vector

    project = Path(__file__).resolve().parents[1]
    source = project / "Exports/Rankin/EditorRankin.obj"
    output = project / "Evidence/P1/room-probe"
    output.mkdir(parents=True, exist_ok=True)
    import_settings = {
        "forward_axis": "Y", "up_axis": "Z", "global_scale": 1.0,
        "clamp_size": 0.0, "use_split_objects": False, "use_split_groups": True,
        "validate_meshes": True,
    }
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.wm.obj_import(filepath=str(source), **import_settings)
    imported = list(bpy.context.scene.objects)
    sample = bpy.data.objects["StaticMeshActor277"]
    anchor = Vector((1488.0, -416.812988, -2368.0))
    anchor_error = min((vertex.co - anchor).length for vertex in sample.data.vertices)
    if anchor_error > 0.001:
        raise ValueError("Native OBJ import changed the confirmed numeric coordinate frame")

    selected = []
    crossing_props = []
    for obj in imported:
        lower, upper = bounds(obj)
        intersects = all(upper[axis] >= OBJ_MIN[axis] and lower[axis] <= OBJ_MAX[axis] for axis in range(3))
        if obj.name == "BSP" or intersects:
            selected.append(obj)
            if obj.name != "BSP" and any(lower[axis] < OBJ_MIN[axis] or upper[axis] > OBJ_MAX[axis] for axis in range(3)):
                crossing_props.append(obj.name)
        else:
            mesh = obj.data
            bpy.data.objects.remove(obj, do_unlink=True)
            bpy.data.meshes.remove(mesh)

    bsp = bpy.data.objects["BSP"]
    bsp_before = {"vertices": len(bsp.data.vertices), "faces": len(bsp.data.polygons)}
    bm = bmesh.new()
    bm.from_mesh(bsp.data)
    for axis in range(3):
        normal = [0.0, 0.0, 0.0]
        normal[axis] = 1.0
        for boundary, lower_plane in ((OBJ_MIN[axis], True), (OBJ_MAX[axis], False)):
            point = [0.0, 0.0, 0.0]
            point[axis] = boundary
            bmesh.ops.bisect_plane(
                bm, geom=[*bm.verts, *bm.edges, *bm.faces], dist=0.00001,
                plane_co=point, plane_no=normal,
                clear_inner=lower_plane, clear_outer=not lower_plane,
            )
    boundary_edges = sum(len(edge.link_faces) == 1 for edge in bm.edges)
    bm.to_mesh(bsp.data)
    bm.free()
    bsp.data.update()
    lower, upper = bounds(bsp)
    if not bsp.data.polygons or any(lower[axis] < OBJ_MIN[axis] - 0.001 or upper[axis] > OBJ_MAX[axis] + 0.001 for axis in range(3)):
        raise ValueError("BSP clipping failed the fixed atrium bounds contract")

    # OBJ=(source X, source Z, source Y). Reflection needs a winding reversal.
    swap = Matrix(((1, 0, 0, 0), (0, 0, 1, 0), (0, 1, 0, 0), (0, 0, 0, 1)))
    minimum_normal_dot = 1.0
    checked_normals = 0
    orientation_failures = []
    zero_area_faces = []
    for obj in selected:
        mesh = obj.data
        uv_layer = mesh.uv_layers.active
        before_corners = Counter(
            tuple(swap @ mesh.vertices[loop.vertex_index].co) + tuple(uv_layer.data[index].uv)
            for index, loop in enumerate(mesh.loops)
        )
        expected_normals = [swap.to_3x3() @ face.normal.copy() for face in mesh.polygons]
        mesh.transform(swap)
        mesh.flip_normals()
        mesh.update()
        after_corners = Counter(
            tuple(mesh.vertices[loop.vertex_index].co) + tuple(uv_layer.data[index].uv)
            for index, loop in enumerate(mesh.loops)
        )
        if before_corners != after_corners:
            raise ValueError("Coordinate/winding conversion changed a position/UV association")
        for expected, face in zip(expected_normals, mesh.polygons):
            if face.area == 0.0:
                zero_area_faces.append({"object": obj.name, "face": face.index})
                continue
            if expected.length_squared > 0.000000000001:
                normal_dot = expected.normalized().dot(face.normal)
                minimum_normal_dot = min(minimum_normal_dot, normal_dot)
                if normal_dot < 0.999:
                    orientation_failures.append({"object": obj.name, "face": face.index, "dot": normal_dot, "expected": list(expected), "actual": list(face.normal)})
                checked_normals += 1
    if minimum_normal_dot < 0.999:
        print(json.dumps({"orientation_failure_count": len(orientation_failures), "first_failures": orientation_failures[:8]}))
        raise ValueError("Reflected surface orientation was not preserved by winding reversal")
    expected = snapshot(selected)

    scene = bpy.context.scene
    scene.unit_settings.system = "NONE"
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x = 1200
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.filepath = str(output / "FlakAtrium-geometry.png")
    scene.display.shading.light = "STUDIO"
    scene.display.shading.color_type = "SINGLE"
    scene.display.shading.single_color = (0.65, 0.68, 0.72)
    scene.display.shading.show_shadows = True
    scene.display.shading.show_cavity = True
    scene.display.shading.cavity_type = "BOTH"
    camera = bpy.data.objects.new("GeometryPreview", bpy.data.cameras.new("GeometryPreview"))
    scene.collection.objects.link(camera)
    camera.location = (1740.0, -2460.0, -420.0)
    camera.rotation_euler = (Vector((1050.0, -1730.0, -160.0)) - camera.location).to_track_quat("-Z", "Y").to_euler()
    camera.data.lens = 24.0
    camera.data.clip_start = 1.0
    camera.data.clip_end = 20000.0
    scene.camera = camera
    bpy.context.preferences.filepaths.save_version = 0
    blend_path = output / "FlakAtrium-geometry.blend"
    fbx_path = output / "FlakAtrium-geometry.fbx"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    blend_check = verify(expected, snapshot(meshes))
    for obj in bpy.context.scene.objects:
        obj.select_set(obj.type == "MESH")
    export_settings = {
        "global_scale": 1.0, "apply_unit_scale": False, "apply_scale_options": "FBX_SCALE_UNITS",
        "axis_forward": "Y", "axis_up": "Z", "use_selection": True,
        "object_types": {"MESH"}, "use_mesh_modifiers": False, "mesh_smooth_type": "FACE", "bake_anim": False,
    }
    bpy.ops.export_scene.fbx(filepath=str(fbx_path), **export_settings)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(fbx_path), use_anim=False, use_image_search=False)
    actual_fbx = snapshot([obj for obj in bpy.context.scene.objects if obj.type == "MESH"])
    fbx_check = verify(expected, actual_fbx)
    bsp_summary = expected["BSP"]
    context_min = [min(item["bounds_min_source_units"][axis] for item in expected.values()) for axis in range(3)]
    context_max = [max(item["bounds_max_source_units"][axis] for item in expected.values()) for axis in range(3)]
    report = {
        "probe": "Fixed Flak atrium preliminary geometry handoff",
        "source": str(source.relative_to(project)), "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "blender_version": bpy.app.version_string, "native_import_settings": import_settings,
        "native_import_groups": len(imported), "numeric_import_anchor_error": anchor_error,
        "obj_selection_bounds_min": OBJ_MIN, "obj_selection_bounds_max": OBJ_MAX,
        "coordinate_conversion": "Swap mesh Y/Z to recover source XYZ; reverse polygon winding; preserve imported OBJ UVs without another V flip.",
        "bsp_before_clipping": bsp_before, "bsp_after_clipping": {key: value for key, value in bsp_summary.items() if not key.startswith("_")},
        "clip_policy": "Six native bmesh bisect planes, no cap fills; intersecting props/movers retained whole as context.",
        "bsp_boundary_edges_after_clip": boundary_edges,
        "whole_context_groups_crossing_box": sorted(crossing_props),
        "context_bounds_min_source_units": context_min, "context_bounds_max_source_units": context_max,
        "surface_orientation_check": {"passed": True, "nonzero_area_faces_checked": checked_normals, "minimum_reflected_normal_dot": minimum_normal_dot, "position_uv_associations_preserved": True, "source_zero_area_faces_retained": zero_area_faces},
        "selected_objects": {name: {key: value for key, value in item.items() if not key.startswith("_")} for name, item in expected.items()},
        "geometry_totals": {key: sum(item[key] for item in expected.values()) for key in ("vertices", "faces", "uv_corners")},
        "geometry_preview_camera_source_xyz": {"location": [1740.0, -2460.0, -420.0], "target": [1050.0, -1730.0, -160.0], "lens_mm": 24.0},
        "export_settings": {**export_settings, "object_types": ["MESH"]},
        "fbx_unit_metadata": "100 centimeters per Blender unit is transport metadata; source-to-UE5 physical scale remains pending.",
        "float_serialization_tolerances": {"position_source_units": 0.001, "uv": 0.000001},
        "saved_blend_check": blend_check, "fbx_round_trip_check": fbx_check,
        "fbx_material_slot_aliases": {
            name: [{"slot": index, "original_obj_label": original, "fbx_label": exported} for index, (original, exported) in enumerate(zip(item["material_slots"], actual_fbx[name]["material_slots"]))]
            for name, item in expected.items()
        },
        "passed": blend_check["passed"] and fbx_check["passed"],
        "unverified": ["UE5 import, physical scale, and collision", "Original normals/smoothing, textures, and material appearance", "Native short material label package identity; stock FBX exporter also abbreviates four long labels", "UV alignment on generated BSP cut boundaries", "Mover animation and gameplay"],
    }
    if report["passed"]:
        bpy.ops.wm.open_mainfile(filepath=str(blend_path))
        bpy.ops.render.render(write_still=True)
    report["geometry_preview_exists"] = (output / "FlakAtrium-geometry.png").is_file()
    report["artifacts"] = {
        path.name: {"bytes": path.stat().st_size, "sha256": sha256(path.read_bytes()).hexdigest()}
        for path in (blend_path, fbx_path, output / "FlakAtrium-geometry.png") if path.is_file()
    }
    (output / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "selected_groups": len(expected), "bsp_faces": bsp_summary["faces"], "geometry_totals": report["geometry_totals"], "blend": blend_check, "fbx": fbx_check, "preview": report["geometry_preview_exists"]}))
    if not report["passed"]:
        raise ValueError("Room geometry verification failed; inspect validation.json")


if __name__ == "__main__":
    main()

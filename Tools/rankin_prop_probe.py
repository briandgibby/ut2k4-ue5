"""Fixed Brace01HA recovery probe; run with Blender --background --python."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path


def parse_triangles(text):
    """Read the native UCC Triangle/Texture/SmoothingMask/Vertex records."""
    triangles = []
    triangle = None
    for line in text.splitlines():
        fields = line.split()
        if fields == ["Begin", "Triangle"]:
            triangle = {"vertices": {}}
        elif fields == ["End", "Triangle"]:
            if (
                triangle is None
                or "material" not in triangle
                or "smoothing_mask" not in triangle
                or set(triangle["vertices"]) != {0, 1, 2}
                or any(len(vertex) != 5 for vertex in triangle["vertices"].values())
            ):
                raise ValueError("Incomplete triangle in native mesh export")
            triangle["vertices"] = [triangle["vertices"][index] for index in range(3)]
            triangles.append(triangle)
            triangle = None
        elif triangle is not None and fields:
            if fields[0] == "Texture":
                triangle["material"] = fields[1]
            elif fields[0] == "SmoothingMask":
                triangle["smoothing_mask"] = int(fields[1])
            elif fields[0] == "Vertex":
                triangle["vertices"][int(fields[1])] = tuple(map(float, fields[2:]))
    if triangle is not None:
        raise ValueError("Incomplete triangle at end of native mesh export")
    return triangles


def mesh_records(obj):
    """Read actual Blender polygon corners in source coordinates."""
    uv_layer = obj.data.uv_layers.active
    records = []
    materials = []
    for polygon in obj.data.polygons:
        materials.append(obj.data.materials[polygon.material_index].name)
        for loop_index in polygon.loop_indices:
            loop = obj.data.loops[loop_index]
            position = obj.matrix_world @ obj.data.vertices[loop.vertex_index].co
            records.append(tuple(position) + tuple(uv_layer.data[loop_index].uv))
    return records, materials


def comparison(obj, expected, expected_materials):
    records, materials = mesh_records(obj)
    lower = [min(record[axis] for record in records) for axis in range(3)]
    upper = [max(record[axis] for record in records) for axis in range(3)]
    position_error = max(
        abs(actual[axis] - reference[axis])
        for actual, reference in zip(records, expected)
        for axis in range(3)
    )
    uv_error = max(
        abs(actual[axis] - reference[axis])
        for actual, reference in zip(records, expected)
        for axis in (3, 4)
    )
    passed = (
        len(records) == len(expected)
        and len(obj.data.polygons) == 288
        and all(len(polygon.vertices) == 3 for polygon in obj.data.polygons)
        and materials == expected_materials
        and position_error <= 0.0001
        and uv_error <= 0.000001
    )
    return {
        "passed": passed,
        "mesh_vertices": len(obj.data.vertices),
        "triangles": len(obj.data.polygons),
        "uv_corners": len(records),
        "bounds_min_source_units": lower,
        "bounds_max_source_units": upper,
        "dimensions_source_units": [upper[axis] - lower[axis] for axis in range(3)],
        "uv_min": [min(record[axis] for record in records) for axis in (3, 4)],
        "uv_max": [max(record[axis] for record in records) for axis in (3, 4)],
        "material_coverage": dict(Counter(materials)),
        "smooth_faces": sum(polygon.use_smooth for polygon in obj.data.polygons),
        "max_position_error_source_units": position_error,
        "max_uv_error": uv_error,
    }


def main():
    import bpy

    project = Path(__file__).resolve().parents[1]
    source = project / "Exports/Rankin/MeshT3DProbe/Beams.Brace01HA.t3d"
    output = project / "Evidence/P1/prop-probe"
    output.mkdir(parents=True, exist_ok=True)
    triangles = parse_triangles(source.read_text(encoding="utf-8"))
    corners = [vertex for triangle in triangles for vertex in triangle["vertices"]]
    materials = [triangle["material"] for triangle in triangles]

    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.context.scene.unit_settings.system = "NONE"
    mesh = bpy.data.meshes.new("Brace01HA")
    mesh.from_pydata(
        [corner[:3] for corner in corners],
        [],
        [tuple(range(index, index + 3)) for index in range(0, len(corners), 3)],
    )
    mesh.update()
    mesh.materials.append(bpy.data.materials.new(materials[0]))
    uv_layer = mesh.uv_layers.new(name="SourceUV")
    for polygon, triangle in zip(mesh.polygons, triangles):
        polygon.use_smooth = triangle["smoothing_mask"] != 0
        for loop_index, corner in zip(polygon.loop_indices, triangle["vertices"]):
            uv_layer.data[loop_index].uv = corner[3:]
    obj = bpy.data.objects.new("Brace01HA", mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    blend_path = output / "Brace01HA.blend"
    fbx_path = output / "Brace01HA.fbx"
    bpy.ops.wm.save_as_mainfile(filepath=str(blend_path))

    # Reopen the saved native artifact before checking and exporting it.
    bpy.ops.wm.open_mainfile(filepath=str(blend_path))
    obj = bpy.data.objects["Brace01HA"]
    blend_result = comparison(obj, corners, materials)
    export_settings = {
        "global_scale": 1.0,
        "apply_unit_scale": False,
        "apply_scale_options": "FBX_SCALE_UNITS",
        "axis_forward": "Y",
        "axis_up": "Z",
        "use_selection": True,
        "object_types": {"MESH"},
        "use_mesh_modifiers": False,
        "mesh_smooth_type": "FACE",
        "bake_anim": False,
    }
    bpy.ops.export_scene.fbx(filepath=str(fbx_path), **export_settings)
    # Import into a clean scene to check the file, not the pre-export mesh.
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.fbx(filepath=str(fbx_path), use_anim=False, use_image_search=False)
    imported_meshes = [obj for obj in bpy.context.scene.objects if obj.type == "MESH"]
    if len(imported_meshes) != 1:
        raise ValueError("FBX round-trip did not produce the single probe mesh")
    fbx_result = comparison(imported_meshes[0], corners, materials)
    report = {
        "probe": "Beams.Brace01HA native UCC triangulated T3D",
        "source": str(source.relative_to(project)),
        "source_sha256": sha256(source.read_bytes()).hexdigest(),
        "blender_version": bpy.app.version_string,
        "source_triangles": len(triangles),
        "source_corner_records": len(corners),
        "source_material_coverage": dict(Counter(materials)),
        "source_smoothing_masks": dict(Counter(str(triangle["smoothing_mask"]) for triangle in triangles)),
        "coordinate_policy": "Unchanged source XYZ and UV values; no instance placement or physical scale calibration.",
        "fbx_unit_metadata": "100 centimeters per Blender unit is transport metadata; source-to-UE5 physical scale remains pending.",
        "export_settings": {**export_settings, "object_types": sorted(export_settings["object_types"])},
        "float_serialization_tolerances": {"position_source_units": 0.0001, "uv": 0.000001},
        "saved_blend": blend_result,
        "fbx_round_trip": fbx_result,
        "passed": blend_result["passed"] and fbx_result["passed"],
        "unverified": [
            "UE5 import, pivot/axis mapping, and physical scale calibration",
            "Original vertex normals and shading fidelity; Blender derives normals from independent triangle vertices",
            "Original collision; no collision has been reconstructed",
            "Texture pixels and material appearance; only the exported material object name is retained",
        ],
        "artifacts": {
            path.name: {"bytes": path.stat().st_size, "sha256": sha256(path.read_bytes()).hexdigest()}
            for path in (blend_path, fbx_path)
        },
    }
    (output / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"prop_probe_passed": report["passed"], "saved_blend": blend_result, "fbx_round_trip": fbx_result}))
    if not report["passed"]:
        raise ValueError("Prop probe validation failed; inspect validation.json")


if __name__ == "__main__":
    main()

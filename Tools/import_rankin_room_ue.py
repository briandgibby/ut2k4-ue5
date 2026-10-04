"""Fixed atrium transport probe; execute inside the UE5 Python commandlet."""

from hashlib import sha256
import json
from pathlib import Path

import unreal


PROJECT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT / "Evidence/P1/room-probe/FlakAtrium-geometry.fbx"
OUTPUT = PROJECT / "Evidence/P1/ue-import"
ASSET_FOLDER = "/Game/RankinRecovery"
MESH_NAME = "SM_FlakAtrium_Transport"
LEVEL_PATH = ASSET_FOLDER + "/L_FlakAtrium_Transport"
ACTOR_LABEL = "FlakAtrium_NumericTransport"


def vector_values(vector):
    return [vector.x, vector.y, vector.z]


def measure(mesh):
    box = mesh.get_bounding_box()
    materials = mesh.get_editor_property("static_materials")
    return {
        "asset": mesh.get_path_name(),
        "bounds_min_ue_cm": vector_values(box.min),
        "bounds_max_ue_cm": vector_values(box.max),
        "lod_count": mesh.get_num_lods(),
        "lod0_render_vertices": mesh.get_num_vertices(0),
        "lod0_render_triangles": mesh.get_num_triangles(0),
        "lod0_uv_channels": mesh.get_num_tex_coords(0),
        "lod0_sections": mesh.get_num_sections(0),
        "material_slots": [
            {
                "index": index,
                "slot_name": str(material.material_slot_name),
                "imported_slot_name": str(material.get_editor_property("imported_material_slot_name")),
                "material": material.material_interface.get_path_name() if material.material_interface else None,
            }
            for index, material in enumerate(materials)
        ],
    }


def main():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source_report = json.loads((PROJECT / "Evidence/P1/room-probe/validation.json").read_text(encoding="utf-8"))
    if not source_report["passed"]:
        raise RuntimeError("Blender atrium validation did not pass")
    source_hash = sha256(SOURCE.read_bytes()).hexdigest()
    if source_hash != source_report["artifacts"][SOURCE.name]["sha256"]:
        raise RuntimeError("Atrium FBX no longer matches its verified Blender report")

    assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    levels = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    level_ready = levels.load_level(LEVEL_PATH) if assets.does_asset_exist(LEVEL_PATH) else levels.new_level(LEVEL_PATH)
    if not level_ready:
        raise RuntimeError("Could not open the separate atrium inspection level")
    world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
    unreal.SystemLibrary.execute_console_command(world, "Interchange.FeatureFlags.Import.FBX 0")

    options = unreal.FbxImportUI()
    options.set_editor_property("automated_import_should_detect_type", False)
    options.set_editor_property("mesh_type_to_import", unreal.FBXImportType.FBXIT_STATIC_MESH)
    options.set_editor_property("original_import_type", unreal.FBXImportType.FBXIT_STATIC_MESH)
    options.set_editor_property("import_as_skeletal", False)
    options.set_editor_property("import_animations", False)
    options.set_editor_property("import_materials", False)
    options.set_editor_property("import_textures", False)
    import_settings = {
        "combine_meshes": True,
        "transform_vertex_to_absolute": True,
        "bake_pivot_in_vertex": False,
        "convert_scene": False,
        "convert_scene_unit": False,
        "force_front_x_axis": False,
        "import_uniform_scale": 1.0,
        "build_nanite": False,
        "generate_lightmap_u_vs": False,
        "auto_generate_collision": False,
        "remove_degenerates": False,
    }
    static_options = options.get_editor_property("static_mesh_import_data")
    for property_name, value in import_settings.items():
        static_options.set_editor_property(property_name, value)
    static_options.set_editor_property("import_translation", unreal.Vector(0, 0, 0))
    static_options.set_editor_property("import_rotation", unreal.Rotator(0, 0, 0))
    static_options.set_editor_property("normal_import_method", unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
    task = unreal.AssetImportTask()
    task.set_editor_property("filename", str(SOURCE))
    task.set_editor_property("destination_path", ASSET_FOLDER)
    task.set_editor_property("destination_name", MESH_NAME)
    task.set_editor_property("automated", True)
    task.set_editor_property("replace_existing", True)
    task.set_editor_property("replace_existing_settings", True)
    task.set_editor_property("save", True)
    task.set_editor_property("async_", False)
    task.set_editor_property("factory", unreal.FbxFactory())
    task.set_editor_property("options", options)
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])
    meshes = [obj for obj in task.get_objects() if isinstance(obj, unreal.StaticMesh)]
    if len(meshes) != 1:
        raise RuntimeError("Fixed legacy import did not create the single combined static mesh")
    mesh = meshes[0]
    import_data = mesh.get_editor_property("asset_import_data")
    if import_data.get_class().get_name() != "FbxStaticMeshImportData":
        raise RuntimeError("Import did not use the requested legacy FBX settings")
    stored_settings = {property_name: import_data.get_editor_property(property_name) for property_name in import_settings}

    inspection_actor = next((actor for actor in actors.get_all_level_actors() if actor.get_actor_label() == ACTOR_LABEL), None)
    if inspection_actor is None:
        inspection_actor = actors.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(0, 0, 0), unreal.Rotator(0, 0, 0))
    if inspection_actor is None:
        raise RuntimeError("Could not spawn the native atrium inspection actor")
    inspection_actor.set_actor_label(ACTOR_LABEL)
    inspection_actor.set_actor_location(unreal.Vector(0, 0, 0), False, False)
    inspection_actor.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
    inspection_actor.set_actor_scale3d(unreal.Vector(1, 1, 1))
    component = inspection_actor.get_component_by_class(unreal.StaticMeshComponent)
    component.set_static_mesh(mesh)
    component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    asset_saved = assets.save_loaded_asset(mesh, only_if_is_dirty=False)
    level_saved = levels.save_current_level()
    measured = measure(mesh)

    source_min = source_report["context_bounds_min_source_units"]
    source_max = source_report["context_bounds_max_source_units"]
    actual_min = measured["bounds_min_ue_cm"]
    actual_max = measured["bounds_max_ue_cm"]
    dimensions = [actual_max[axis] - actual_min[axis] for axis in range(3)]
    numeric_ratios = [dimensions[axis] / (source_max[axis] - source_min[axis]) for axis in range(3)]
    identity_error = max(abs(actual_min[axis] - source_min[axis]) for axis in range(3))
    identity_error = max(identity_error, *(abs(actual_max[axis] - source_max[axis]) for axis in range(3)))
    mirrored_min = [source_min[0], -source_max[1], source_min[2]]
    mirrored_max = [source_max[0], -source_min[1], source_max[2]]
    mirrored_error = max(abs(actual_min[axis] - mirrored_min[axis]) for axis in range(3))
    mirrored_error = max(mirrored_error, *(abs(actual_max[axis] - mirrored_max[axis]) for axis in range(3)))
    axis_mapping = "UE XYZ = source XYZ" if identity_error <= 0.01 else "UE XYZ = (source X, -source Y, source Z)" if mirrored_error <= 0.01 else "Unresolved; inspect measured bounds before claiming coordinate preservation"
    numeric_transport_passed = min(identity_error, mirrored_error) <= 0.01 and max(abs(ratio - 1.0) for ratio in numeric_ratios) <= 0.0001
    report = {
        "probe": "Fixed combined Flak atrium UE5 legacy FBX numeric transport",
        "engine_version": unreal.SystemLibrary.get_engine_version(),
        "source": str(SOURCE.relative_to(PROJECT)), "source_sha256": source_hash,
        "source_nodes": len(source_report["selected_objects"]),
        "source_bounds_min_source_units": source_min, "source_bounds_max_source_units": source_max,
        "factory": "FbxFactory", "actual_import_data_class": import_data.get_class().get_name(),
        "requested_import_settings": import_settings, "stored_import_settings": stored_settings,
        "import_materials": False, "import_textures": False,
        "level": LEVEL_PATH, "actor_label": ACTOR_LABEL, "actor_transform": "Origin, zero rotation, scale1; collision disabled",
        "asset_saved": asset_saved, "level_saved": level_saved,
        "measurements": measured,
        "numeric_scale_ratios_xyz": numeric_ratios,
        "observed_axis_mapping_from_bounds": axis_mapping,
        "identity_bounds_error_ue_cm": identity_error,
        "y_reflection_bounds_error_ue_cm": mirrored_error,
        "numeric_transport_passed": numeric_transport_passed,
        "scale_policy": "Provisional numeric 1 source unit to 1 UE centimeter; FBX scene-unit conversion disabled. Physical UT2004-to-UE5 scale calibration remains pending.",
        "unverified": ["Physical scale and anchor/landmark calibration", "Per-corner UE UV values and original texture alignment", "Original normals, shading, textures and materials", "Collision/navigation, movers, gameplay and runtime acceptance", "Fresh-process serialized asset reload; root UI inspection follows"],
    }
    (OUTPUT / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    unreal.log(json.dumps({"asset_saved": asset_saved, "level_saved": level_saved, "numeric_transport_passed": numeric_transport_passed, "axis_mapping": axis_mapping, "measurements": measured, "numeric_scale_ratios_xyz": numeric_ratios}))
    if not asset_saved or not level_saved or not numeric_transport_passed:
        raise RuntimeError("Atrium numeric transport probe needs review; inspect validation.json")


if __name__ == "__main__":
    main()

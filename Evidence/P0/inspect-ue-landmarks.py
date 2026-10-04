"""Read-only native UE check of fixed atrium source surface samples.

Run in the already-open project's native Python field. No assets are saved.
"""
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

import unreal

ROOT = Path(r"C:\Users\brian\git-projects\ut2k4-ue5")
SOURCE = ROOT / "Exports/Rankin/EditorRankin.obj"
ASSET = ROOT / "Prototype/Content/RankinRecovery/SM_FlakAtrium_Transport.uasset"
SAMPLES = [
    ("BSP-floor-A", "BSP", 4866, 11595),
    ("BSP-floor-B", "BSP", 4867, 11596),
    ("BSP-floor-C", "BSP", 5046, 12028),
    ("BSP-ceiling-D", "BSP", 4809, 11461),
    ("Flak base", "xWeaponBase2", 311217, 826583),
    ("Central brace", "StaticMeshActor426", 256928, 681721),
    ("North brace", "StaticMeshActor425", 257792, 684026),
    ("South brace", "StaticMeshActor419", 258656, 686331),
    ("Lamp", "StaticMeshActor538", 329901, 876429),
    ("Second lamp", "StaticMeshActor539", 330435, 877854),
    ("Window 167", "StaticMeshActor167", 45712, 118239),
    ("Window 168", "StaticMeshActor168", 46720, 120928),
    ("Window 128", "StaticMeshActor128", 57664, 150122),
    ("Window 129", "StaticMeshActor129", 58672, 152811),
]

source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
if source_hash != "a6a342e67b700d95513767b2582787ae84f549fcb24836eba5544d6cf9162275":
    raise RuntimeError("Source OBJ changed from the retained transport evidence")
asset_before = hashlib.sha256(ASSET.read_bytes()).hexdigest()
by_index = {sample[2]: sample for sample in SAMPLES}
source_points = {}
group = None
vertex_index = 0
with SOURCE.open(encoding="utf-8") as stream:
    for line_number, line in enumerate(stream, 1):
        if line.startswith("g "):
            group = line.split()[1]
        elif line.startswith("v "):
            vertex_index += 1
            if vertex_index in by_index:
                sample = by_index[vertex_index]
                if group != sample[1] or line_number != sample[3]:
                    raise RuntimeError(f"Source provenance mismatch for {sample[0]}")
                raw = [float(value) for value in line.split()[1:4]]
                source_points[vertex_index] = (raw, [raw[0], raw[2], raw[1]])
if len(source_points) != len(SAMPLES):
    raise RuntimeError("Source sample missing")

mesh = unreal.load_asset("/Game/RankinRecovery/SM_FlakAtrium_Transport")
description = mesh.get_static_mesh_description(0)
vertices = []
for index in range(description.get_vertex_count()):
    vertex_id = unreal.VertexID(index)
    if description.is_vertex_valid(vertex_id):
        point = description.get_vertex_position(vertex_id)
        vertices.append((index, [point.x, point.y, point.z]))

results = []
for name, group, source_index, source_line in SAMPLES:
    raw, source = source_points[source_index]
    expected = [source[0], -source[1], source[2]]
    native_id, measured = min(vertices, key=lambda item: math.dist(item[1], expected))
    error = math.dist(measured, expected)
    results.append({
        "sample": name, "source_group": group,
        "obj_global_vertex_index_1_based": source_index,
        "obj_vertex_line_1_based": source_line,
        "raw_obj_xyz": raw, "source_xyz": source,
        "expected_numeric_ue_xyz": expected,
        "native_mesh_description_vertex_id": native_id,
        "measured_mesh_local_ue_xyz": measured,
        "distance_error_numeric_ue_units": error,
    })

asset_after = hashlib.sha256(ASSET.read_bytes()).hexdigest()
report = {
    "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
    "method": "Existing interactive editor; native saved StaticMeshDescription LOD0 vertex readback; nearest measured point to each fixed source sample",
    "engine_version": unreal.SystemLibrary.get_engine_version(),
    "source": str(SOURCE.relative_to(ROOT)), "source_sha256": source_hash,
    "asset": "/Game/RankinRecovery/SM_FlakAtrium_Transport",
    "asset_sha256_before": asset_before, "asset_sha256_after": asset_after,
    "asset_unchanged": asset_before == asset_after,
    "mesh_description_vertex_count": description.get_vertex_count(),
    "valid_vertices_searched": len(vertices),
    "mapping_tested": "UE XYZ = (source X, -source Y, source Z), numeric scale 1",
    "numeric_probe_threshold": 0.001,
    "threshold_status": "Readback precision check only; does not lock owner D-02 tolerances",
    "samples": results,
    "max_sample_error_numeric_ue_units": max(item["distance_error_numeric_ue_units"] for item in results),
    "sample_correspondence_passed": all(item["distance_error_numeric_ue_units"] <= 0.001 for item in results),
    "limits": [
        "Actual source mesh corners, not actor origins or pivots; combined UE mesh has no per-source-actor identity",
        "Four noncoplanar BSP samples and ten landmark-group corners; not all vertices or full-map landmarks",
        "MeshDescription source geometry readback; not render-buffer per-corner UV or normal validation",
        "Physical centimeters per source unit remains an owner design/calibration decision",
        "Collision, runtime gameplay, matched cameras, textures and P0/P1 acceptance remain open",
    ],
}
(ROOT / "Evidence/P0/ue-landmark-samples.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
unreal.log(f"P0_LANDMARK_SAMPLES passed={report['sample_correspondence_passed']} max_error={report['max_sample_error_numeric_ue_units']} asset_unchanged={report['asset_unchanged']}")

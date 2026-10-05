# Rankin room source reference

Measured on 2026-10-04 from the installed UT2004 build 3369 map and the protected-copy UCC exports; runtime update: 2026-10-05. The owner locked DM-Rankin, the Flak atrium pilot, D-02 comparison targets, and a 2 cm/source-unit design scale. Applied UE5 scale, rendered comparison, collision/traversal, and phase acceptance remain pending.

## Source evidence

| Source | Size | SHA-256 |
|---|---:|---|
| Original `Maps/DM-Rankin.ut2` | 13,400,320 bytes | `A8F7993BDD14B5FB0B6F75CB56E62F1C3917A8339E378C18B1439808444DFF98` |
| [Level and actor export](../Exports/Rankin/myLevel.t3d) | 3,195,480 bytes | `657E6677B81CBB23CA4DB01D5CC1A1F53A889AFF55CE226FE3555E80D2102005` |
| [Brace mesh export](../Exports/Rankin/MeshT3DProbe/Beams.Brace01HA.t3d) | 92,288 bytes | `EF2BE45B757C2ECF868033A4B3A38D0816916E564ACE08780BB9EE0958A185CE` |

The level export identifies the title as Rankin and the author as Sjoerd De Jong. The project coordinator ran the exports from `ReferenceGame/System` and reported exit code 0, zero warnings, and zero errors. Analysis here reads the exported files; it does not establish a successful UE5 import.

The authorized installed-executable fallback now supplies a [native runtime parameter baseline](../Evidence/P0/runtime-parameter-baseline.json): build 3369, Rankin, `XGame.xDeathMatch`, GameSpeed `1`, TimeDilation `1.1`, zero reported bots, and the active default volume's gravity `(0,0,-950)` and friction values. Live camera FOV is `90`; the inherited xPlayer class default `85` is a separate row. Startup metadata warnings remain open with causes unproven. [Gameplay reference](gameplay-reference.md) separates these observations from unaccepted trajectory and collision behavior.

## Selected pilot: the Flak atrium

Use the tall room containing `xWeaponBase2` (`XWeapons.FlakCannon`) and `ZoneInfo7`. Its enclosing subtractive brush is `Brush42`, referring to `DM-Rankin.Model43` (level export line 1612).

All coordinates below are UT2004 source units. The nominal boundary is rounded to the source grid; exported vertex noise is below 0.001 unit. At the locked design scale, the calculated room dimensions are `2304 × 2688 × 3072` cm. This is an arithmetic expectation, not an applied-scale UE5 measurement.

| Measurement | Source value |
|---|---|
| World X range | 768 to 1920 |
| World Y range | -2720 to -1376 |
| World Z range | -512 to 1024 |
| Dimensions | 1152 x 1344 x 1536 |
| Box center | (1344, -2048, 256) |
| Floor-center anchor | (1344, -2048, -512) |
| Brush42 actor location | (1792, -1376, 768) |
| Brush42 PrePivot | (768, 672, 1024) |

Brush42 has no exported rotation or non-unit scale. Its local vertex ranges are X -256 to 896, Y -672 to 672, Z -256 to 1280. The bounds above follow `world = vertex - PrePivot + Location`. Its four walls reference `DM-Rankin.shaiBricks1b`; the ceiling references `HumanoidArchitecture.Ceilings.cel03HA`; the floor references `HumanoidArchitecture.Floors.flr02HA`. Preserve polygon texture origins and TextureU/TextureV vectors when reconstructing its UVs.

The enclosing box is a selection boundary, not the final playable solid. Additional brushes form openings, ledges, and details. Preserve the source CSG order and inspect geometry intersecting the box. Brush42's actor location lies on the Y boundary and is included by an inclusive origin selection. However, actor locations do not define brush or mesh extents; origin selection alone cannot establish the complete room set. Filtering only `ZoneInfo7` also misses relevant geometry and props.

The [one-jump viability run](../Evidence/P0/runtime-jump-viability.json) began with a floor-resting pawn center at `(4724.301758,448,-366.149994)`, outside this box. It does not test atrium routes or clearance; apparent pause/step sampling bias has an unproven cause. The F10 toggle did not produce a crouched-state witness; crouched dimensions are still source-only. Five controlled movement trials per action remain required by the locked D-02 target.

Adjacent subtractive geometry to inspect includes `Brush52` and `Brush53` at the west lower opening, `Brush63` at the adjoining west corridor, and `Brush113` beyond that opening. `Brush337` and `Brush397` lie within the room boundary. Their inclusion requires checking the final CSG result; do not automatically merge the adjoining rooms into the pilot.

## Placement landmarks

These are actor origins for matching placement, not visible surface measurements. Keep their source actor names in the pilot so comparisons can identify the same object.

| Actor | Landmark | Location (X, Y, Z) |
|---|---|---|
| xWeaponBase2 | Flak base | (1166, -1932, -510) |
| StaticMeshActor426 | Central brace | (1376, -1864, 440) |
| StaticMeshActor425 | North brace | (1376, -1512, 440) |
| StaticMeshActor419 | South brace | (1376, -2208, 440) |
| StaticMeshActor538 | Lamp | (1112.000244, -2552, 348) |
| StaticMeshActor539 | Second lamp | (1672.000244, -2552, 348) |
| StaticMeshActor167 | Upper window frame | (1536, -2000, 983.999878) |
| StaticMeshActor168 | Upper window frame | (1536, -1712, 983.999878) |
| StaticMeshActor128 | Upper window frame | (1152, -2000, 983.999878) |
| StaticMeshActor129 | Upper window frame | (1152, -1712, 983.999878) |

The three mini-health origins provide an additional vertical-route check: `MiniHealthPack1` (1536, -2554, -125.285683), `MiniHealthPack2` (1656, -2556, -73.857117), and `MiniHealthPack3` (1793, -2558, -22). This is placement evidence; the route still needs visual and collision verification.

Inclusive actor-origin selection in the box finds 142 actors: 55 brushes, 34 static-mesh actors, 13 lights, 9 path nodes, 6 inventory spots, 4 blocking volumes, 4 scripted triggers, 4 triggers, 3 mini-health packs, 2 each of ambient sounds, emitters, Flak ammo, and jump spots, plus the Flak base and ZoneInfo7. This is an inventory aid, not a complete geometry extraction.

## First fixed mesh sample

Use `HumanoidHardware.Beams.Brace01HA`, already exported by the installed UCC tool. `StaticMeshActor426` is an actual instance in the selected room (level export line 33580):

```text
Location=(X=1376.000000,Y=-1864.000000,Z=440.000000)
Rotation=(Roll=-16384)
DrawScale3D=(X=2.125000,Z=1.250000)
```

The unplaced mesh contains 288 triangles, 864 triangle-corner position/UV records, one material label `HumanoidArchitecture.Bases.bas05bHA`, and `SmoothingMask 1` on every triangle. Its local bounding box is min (-264.000977, -72.977997, -57.874001), max (248, 73.759995, 57.547001).

The [fixed-sample Blender probe](../Evidence/P1/prop-probe/validation.json) preserves local positions, triangle order, UVs, and the material label through saved-Blender and FBX round trips. Instance rotation, non-uniform scale, and UE5 pivot behavior remain separate checks. The T3D contains no explicit vertex normals, tangents, collision hulls, lightmap UV channel, or LODs. Recomputed normals are an approximation until checked against the original. A geometry/UV handoff does not establish collision or shading fidelity.

The representative map-local lamp is `DM-Rankin.hourelamp2azo`. `StaticMeshActor538` uses `Rotation=(Pitch=16384,Yaw=49152)` and `Skins(5)=Shader'DM-Rankin.hourelamp1yellowshader'`. It is a useful later material-slot test, after the simpler brace works.

## Room mesh dependencies

Of the 34 static-mesh actor origins inside the box, 30 reference map-local objects. Exporting only external `.usx` packages cannot recover this room.

| Static mesh reference | Instances with origins inside |
|---|---:|
| DM-Rankin.hourehouteplank | 7 |
| DM-Rankin.hourewindowraamkosijn | 4 |
| DM-Rankin.hourewindowsheet1 | 4 |
| DM-Rankin.hourerechtepillarlang | 3 |
| DM-Rankin.hourewatersheet | 3 |
| HumanoidHardware.Beams.Brace01HA | 3 |
| DM-Rankin.hourelamp2azo | 2 |
| DM-Rankin.hourewallpanel1 | 2 |
| DM-Rankin.houremaybeentllamp | 1 |
| DM-Rankin.hourepijptypedwur | 1 |
| DM-Rankin.houreventthing | 1 |
| DM-Rankin.hourewallpanel2pipes | 1 |
| DM-Rankin.testsheet1 | 1 |
| HumanoidHardware.Beams.jribbedcolumn01HA | 1 |

Start with `DM-Rankin.ut2` for map-local meshes/materials, `StaticMeshes/HumanoidHardware.usx` for the external meshes, and `Textures/HumanoidArchitecture.utx` for the brace, floor, and ceiling texture references. `StaticMeshActor277` overrides the column with `AbaddonArchitecture.Base.bas13go`, requiring `Textures/AbaddonArchitecture.utx`. Map-local shaders, animated water/glass, emitters, and lighting require later inspection; these references are not a complete transitive material dependency manifest.

## Installed export route and supporting sources

Run UCC only in the protected `ReferenceGame/System` copy. The installed `Editor.int` documents `batchexport package.ext classname export_ext path`. The [UT4X maintainer's exporter](https://github.com/xtremexp/UT4X-Converter/blob/master/src/main/java/io/github/xtremexp/ut4converter/export/UCCExporter.java) uses `Level t3d` and `StaticMesh t3d` for this route.

```powershell
.\UCC.exe batchexport "..\Maps\DM-Rankin.ut2" Level T3D "C:\Users\brian\git-projects\ut2k4-ue5\Exports\Rankin"
.\UCC.exe batchexport "..\StaticMeshes\HumanoidHardware.usx" StaticMesh T3D "C:\Users\brian\git-projects\ut2k4-ue5\Exports\Rankin\MeshT3DProbe"
```

For the remaining map-local meshes, use the same StaticMesh T3D command with `..\Maps\DM-Rankin.ut2` and a separate output directory. Batch export is package-wide; choose the named pilot assets from its output.

UCC `Level OBJ` failed with a native exporter fault. Loading the map in the reference editor first succeeds with this bounded native route:

```text
MAP LOAD FILE="..\Maps\DM-Rankin.ut2"
MAP EXPORT FILE="..\..\Exports\Rankin\EditorRankin.obj"
```

Use the editor command field and short relative paths; a long absolute load command was truncated. The [export record](../Evidence/P1/editor-rankin-export.json) preserves the source/export hashes and scope. The 35,293,142-byte OBJ has 730 groups: compiled `BSP` plus 729 actor meshes, including every one of the 664 StaticMeshActors and four movers. Whole-file counts are 494,152 positions, 494,152 UVs, and 163,792 polygon faces. `BSP` contributes 11,218 positions/UVs and 2,814 faces. Mover geometry does not include its animation or collision behavior.

The native mapping is **OBJ = (source X, source Z, source Y)**. `StaticMeshActor277` places local `(112,128,-0.813004)` at source-world `(1488,-2368,-416.813004)` after its Y scale of 1.25; the OBJ vertex is `(1488,-416.812988,-2368)`. Translated brace instances independently confirm the sign. Therefore the room's raw OBJ box is min `(768,-512,-2720)`, max `(1920,1024,-1376)`, with floor anchor `(1344,-512,-2048)`. Eight contained BSP floor polygons lie at raw OBJ Y = -512. These coordinates establish export mapping, not physical UE5 scale.

Blender's [native OBJ importer](https://docs.blender.org/api/current/bpy.ops.wm.html#bpy.ops.wm.obj_import) supports group splitting. Forward Y, Up Z, scale 1, and clamp 0 preserve raw OBJ numbers for checking. Crop the single BSP object only within the fixed room bounds and retain crossing props as labeled context. The OBJ has no normals, smoothing directives, or `mtllib`; material labels omit package paths. Sampled texture V is already negated relative to native mesh T3D, so preserve OBJ UVs during this handoff. Original textures, material identity, normals, collision, and per-corner UE5 UV fidelity remain unverified.

[UModel's maintained source](https://github.com/gildor2/UEViewer/blob/master/UmodelTool/Main.cpp) exposes `-list`, `-export`, `-path=`, `-out=`, and `-gltf` options. Its mesh exporters do not replace the level/actor/brush export. No UModel binary was acquired or run for this pilot; the installed-tool brace sample is sufficient for the first bounded geometry handoff.

## Fixed atrium geometry handoff

The [fixed room script](../Tools/rankin_room_probe.py) imports the native OBJ, clips only BSP to the six room boundaries without caps, retains intersecting actor meshes whole, then swaps Y/Z and reverses polygon winding. It preserves imported OBJ UVs. Repeat with the installed Blender executable:

```powershell
& 'C:\Users\Jack Thompson\AppData\Local\Programs\blender-5.2.2-windows-x64\blender.exe' --background --factory-startup --python-exit-code 1 --python 'C:\Users\brian\git-projects\ut2k4-ue5\Tools\rankin_room_probe.py'
```

The [validation record](../Evidence/P1/room-probe/validation.json) reports 46 retained groups, including clipped BSP with 220 faces. BSP bounds recover source-world min `(768,-2720,-512)`, max `(1920,-1376,1024)`. The saved `.blend` and FBX round trips retain 9,202 faces and 27,804 UV corners with zero measured corner position/UV error and matching polygon material assignments. Four FBX material names are abbreviated; the report retains their source/export mapping. Eight source zero-area triangles remain intact and are excluded from surface-orientation comparisons.

Whole crossing props extend beyond the room box; their names and bounds are recorded separately. The plain geometry preview does not establish original texture appearance, physical scale, collision, or P1 acceptance. Generated clipping-edge UV alignment and mover behavior also remain unverified.

## UE5 numeric transport and saved-level inspection

The [fixed UE import script](../Tools/import_rankin_room_ue.py) uses UE5 5.8.3's built-in Editor Python plugin and legacy `FbxFactory`. It combines the verified 46-node FBX into `/Game/RankinRecovery/SM_FlakAtrium_Transport`. The separate `/Game/RankinRecovery/L_FlakAtrium_Transport` level contains one mesh actor at the origin, zero rotation, scale 1, with collision disabled. Native template assets are preserved.

The [import report](../Evidence/P1/ue-import/validation.json) records exact outer bounds under `UE XYZ = (source X, -source Y, source Z)`: min `(445.5229187,1375.4136963,-552)`, max `(1962.4521484,2776.0627441,1024)`. Dimension ratios are `(1,1,1)` with scene-unit conversion disabled. Bounds are consistent with the Y reflection; individual representative surface samples are checked below. Applying and verifying the locked scale 2 remains pending.

UE reports 20,703 render vertices, 9,392 triangles, one UV channel, and 66 material slots. All slots use `WorldGridMaterial`. Source triangulation has 9,400 candidates; the difference of eight is consistent with the known zero-area triangles, but the omitted triangles have not been individually traced. Per-corner UE UV values, original normals and materials, collision, and traversal remain unverified. The commandlet exited 0 with two near-zero tangent/binormal warnings.

A fresh interactive editor process reopened the serialized level. Native Python readback matched the import bounds and counts; the unlit interior visibly retains the floor, openings, braces, and ledges. [Inspection evidence](../Evidence/P1/ue-import/serialized-inspection.json) and the [native unlit capture](../Evidence/P1/ue-import/FlakAtrium-UE5-unlit.png) record that check. This is a geometry transport proof; P0 calibration and P1 navigable-room acceptance remain open.

Repeat the fixed import with the editor closed:

```powershell
& 'F:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe' 'C:\Users\brian\git-projects\ut2k4-ue5\Prototype\UT2004UE5.uproject' -run=pythonscript '-script=C:\Users\brian\git-projects\ut2k4-ue5\Tools\import_rankin_room_ue.py' -unattended -nop4 -nosplash -nullrhi '-abslog=C:\Users\brian\git-projects\ut2k4-ue5\Evidence\P1\ue-import\measured-import.log'
```

This overwrites the fixed inspection mesh and level; it does not recover materials, collision, or gameplay. Open the project and `/Game/RankinRecovery/L_FlakAtrium_Transport` in Unlit mode to inspect the result.

## Individual saved-UE surface samples — 2026-10-04

The [native readback](../Evidence/P0/ue-landmark-samples.json) checks four noncoplanar BSP vertices and one source corner in each of the ten documented landmark groups against the saved UE mesh's LOD0 `StaticMeshDescription`. The [fixed inspection](../Evidence/P0/inspect-ue-landmarks.py) verifies the retained OBJ hash, group, positive global vertex index and source line before matching measured UE positions. It performs no reimport or asset save.

The four BSP source points are `(1472,-2048,-512)`, `(1472,-1536,-512)`, `(1056,-2336,-512)`, and `(1344,-2208,1024)`. Their measured UE points match `(X,-Y,Z)` exactly. Across all fourteen samples, maximum Euclidean position error is `0.0000004955` numeric UE units. The ten source mesh samples also survive the crop. The original mesh and level hashes remain unchanged.

This extends outer-bounds evidence to individual representative surface points. Actor origins/pivots are not sampled: the combined mesh has no per-source-actor identity. It does not prove every vertex, render-buffer UV/normal fidelity, collision, camera matching, or full-map landmark coverage. The owner selected the 176 cm standing-cylinder correspondence, `s=176/88=2 cm/source unit`, and locked D-02 on 2026-10-05. This is a design choice, not a measured historical physical height. Preserve the scale-1 transport proof; no scale-2 rescale or collision proof has been applied. At scale 2, the calculated standing cylinder radius/half-height are `50/88` cm and source crouched values are `50/58` cm; the UE capsule's different end shape still requires route/clearance checks.

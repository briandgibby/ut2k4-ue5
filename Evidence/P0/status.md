# Initial phase execution status

Updated: 2026-10-04. Scope: Rankin Visual Proof followed by the Rankin Combat Prototype.

The owner authorized execution and selected `C:\Users\brian\git-projects\ut2k4-ue5`. The three planning documents have moved to its `docs/` directory. This path is a Windows profile symlink to `C:\Users\Jack Thompson\git-projects\ut2k4-ue5`; both names address the same project. On 2026-10-04, the owner also authorized an initial commit/push to the private `briandgibby/ut2k4-ue5` repository. Repository exclusions are recorded in [README](../../README.md); the private local credential file and installed ReferenceGame copy are not staged.

## P0 evidence recorded

- [Reference copy record](reference-copy.json): 1,607 protected files were hashed before copying and verified byte-for-byte in `ReferenceGame/`.
- [Original preservation baseline](original-protected-files.csv): file paths, lengths, and SHA-256s. Saves, shader caches, logs, the secondary content folder, DirectX redistributables, and the old docs directory are outside the development copy; they remain untouched in the original installation.
- [Preservation recheck](original-preservation-check.json): all 1,607 protected original files still match; zero changed files after editor/export work.
- [Gameplay reference](../../References/gameplay-reference.md): 36 retained build-3369 scripts with hashes, source-derived movement and Shock Rifle behavior, selected local settings, and an explicit list of unexecuted runtime trials.
- [Room reference](../../References/Rankin-reference.md): proposed Flak atrium, source brush bounds and floor anchor, ten placement landmarks, and map-local/external asset dependencies.
- [Asset manifest](../../References/asset-manifest.csv): initial level-T3D, loaded-editor OBJ, and brace-probe provenance. This is not full-map or final-build dependency coverage.

## Recovery feasibility evidence

These checks prepare P1 while the P0 runtime gate remains incomplete. They do not accept a recovered navigable room.

| Check | Observed result | Evidence |
|---|---|---|
| UCC Level T3D export of Rankin | Passed: 1,949 actors, 3,243 brush polygons, exit 0, no errors/warnings | [Export record](../P1/rankin-export.json) |
| UCC StaticMesh T3D export of HumanoidHardware | Passed: 135 exported objects; selected Brace01HA is present | `../P1/ucc-staticmesh-probe.log` |
| UCC map-local StaticMesh T3D export | Partial: 25 files recovered, including the representative lamp; stopped on `houreceilingpanel` with a file-open error | `../P1/ucc-map-staticmesh-probe.log` |
| UCC Level OBJ export | Failed: native `ULevelExporterOBJ::ExportText` protection fault; no usable OBJ | `../P1/ucc-level-obj-probe.log` |
| Loaded UnrealEd map OBJ export | Passed: compiled BSP plus 729 actor-mesh groups, including all 664 StaticMeshActors and four movers | [Export record](../P1/editor-rankin-export.json) |
| Fixed Brace01HA Blender/FBX handoff | Passed for triangle-corner positions, UVs, triangle count/order, and material name | [Validation](../P1/prop-probe/validation.json) |
| Fixed Flak atrium Blender/FBX handoff | Passed for 46 geometry groups, positions, UVs, and polygon material assignments; clipped BSP has 220 faces | [Validation](../P1/room-probe/validation.json) |
| UE5 fixed atrium import and saved-asset reload | Passed numeric bounds transport; 9,392 render triangles, one UV channel, 66 grid-material slots | [Import record](../P1/ue-import/validation.json), [fresh-editor inspection](../P1/ue-import/serialized-inspection.json) |
| Room collision, source shading, physical scale, and traversal | Unexecuted | Calibrated comparison and navigable-room acceptance remain pending |

The fixed prop probe uses installed UCC and Blender. It adds no converter framework, Blender plugin, or dependency. Its five standard-library tests pass. Shading, collision, textures, placement, and UE5 scale are explicitly unverified.

The loaded-map editor route succeeds where the UCC OBJ commandlet fails. Its native coordinate mapping is `(source X, source Z, source Y)`, verified against a placed unrotated column and translated braces. The OBJ retains UVs and shortened material labels; it contains no original normals or material library. The complete map export is source evidence, not a delivered full-map remake.

The [fixed room script](../../Tools/rankin_room_probe.py) uses Blender's native OBJ importer and six BSP clipping planes. It preserves 45 intersecting actor meshes whole as context, then swaps Y/Z and reverses winding to recover source XYZ. The saved Blender file and FBX each retain 46 groups, 9,202 polygon faces, and 27,804 UV corners, with zero measured corner position/UV error. Eight pre-existing zero-area triangles are retained and recorded. Four material labels are abbreviated in FBX; their changes are recorded, so exact FBX material-name preservation is not claimed. The Blender file retains the native labels.

The room preview is plain geometry. Textures, original shading, collision, physical UE5 scale, generated-cut UV alignment, and navigable-room acceptance remain pending. Crossing props extend beyond the clipped BSP bounds and are identified in the report.

[Geometry preview](../P1/room-probe/FlakAtrium-geometry.png) · [Saved Blender room](../P1/room-probe/FlakAtrium-geometry.blend) · [FBX room](../P1/room-probe/FlakAtrium-geometry.fbx)

The [fixed UE import script](../../Tools/import_rankin_room_ue.py) uses the engine's built-in Editor Python plugin and legacy FBX factory. It combines the 46 source groups into one inspection mesh at `/Game/RankinRecovery/SM_FlakAtrium_Transport`, with collision disabled in `/Game/RankinRecovery/L_FlakAtrium_Transport`. Measured outer bounds match `(source X, -source Y, source Z)` exactly, with dimension ratios `(1,1,1)`. This establishes provisional numeric transport; individual landmarks and physical scale remain uncalibrated. A fresh editor process reopened the saved level and reported the same bounds, render counts, UV-channel count, and material-slot count.

The UE mesh has 9,392 render triangles versus 9,400 source triangulation candidates. The eight-triangle difference is consistent with the eight source zero-area triangles, but their individual removal has not been traced. One UV channel does not establish per-corner UV fidelity. All 66 slots use the engine grid material; original normals, texture appearance, material identity, and collision remain unverified. The native importer reported two near-zero tangent/binormal warnings and zero errors. Its first commandlet attempt failed to spawn an actor from the mesh; the repeat succeeds using a native StaticMeshActor class.

[UE5 unlit geometry capture](../P1/ue-import/FlakAtrium-UE5-unlit.png). This is a transport inspection, not the P2 visual proof.

## Engine and tooling

- Installed source tools: UT2004/UnrealEd/UCC build 3369 and Blender 5.2.2 LTS.
- UE5 5.8.3 is installed at `F:\Program Files\Epic Games\UE_5.8`, verified from `Engine/Build/Build.version`: changelist 58210709, branch `++UE5+Release-5.8`. The owner completed installation.
- The editor and native templates are present. The Blueprint First Person project was created through the native project browser with Variant None, Desktop, and Maximum quality.
- The project is at `Prototype/UT2004UE5.uproject`. [Template setup evidence](ue-project-setup.json) records a successful Play in Editor smoke: spawn, mouse look, jump camera response, and return to the editor. No movement trajectory or performance acceptance is claimed. No packaged UE5 build exists yet.
- Four native template map/Blueprint files still match their creation hashes after the separate atrium import. The built-in PythonScriptPlugin is enabled for Editor targets only.
- UModel is absent. Its official linked Win32 ZIP returned HTTP 404. The bounded native triangle export permits the first geometry handoff; it does not replace missing original normals or collision data.

## Pending P0 gate

The original-game launch check now passes; the remaining runtime work is blocked by the copied executable's Steam load error described below. Capture the walkthrough and controlled gameplay trials, choose/calibrate physical scale, complete landmark/route comparisons, and lock D-02. Rankin loads in the reference editor using `MAP LOAD FILE="..\Maps\DM-Rankin.ut2"`; its geometry exports with `MAP EXPORT FILE="..\..\Exports\Rankin\EditorRankin.obj"`. The earlier long absolute command was truncated by the editor command field. No source/prototype gameplay comparison or failed exporter has been described as passing.

P1 room acceptance and P2 visual work remain pending. Continue with the single Flak atrium and brace sample rather than expanding to a full-map converter.

## Continuation results — 2026-10-04

- [Original smoke](original-game-smoke.json): the installed executable reached its main menu and exited normally. [Capture](original-game-main-menu.png). All 1,607 protected hashes matched immediately before launch; original `UT2004.ini` and `User.ini` hashes are unchanged afterward. [Session preservation check](session-preservation-check.json) also checks all protected originals, four template assets, and the two saved atrium assets.
- [Copied-game launch](reference-game-launch.json): `ReferenceGame/System/UT2004.exe` displayed Steam **Application load error (0x02)** before engine startup. [Error capture](reference-game-launch-error.png). Removing the custom log argument did not resolve it. No Rankin game capture, actual FPS, movement trial, or weapon trial was produced. The precise internal Steam cause is not established.
- [Prepared fallback](reference-launch-fallback.json): use the installed executable with project-local `P0Runtime.ini`/`P0User.ini`, absolute ReferenceGame content/save/cache/music paths, and a project log. **Not executed.** It changes the requested copied-executable boundary and awaits the owner's decision. Native path/config overrides and loaded content must be verified before accepting a trial; recheck protected hashes afterward.
- [Saved UE surface samples](ue-landmark-samples.json): native `StaticMeshDescription` LOD0 readback found all four noncoplanar BSP points and one actual corner from each of ten landmark mesh groups under `(source X, -source Y, source Z)`, numeric scale 1. Maximum Euclidean coordinate error is **0.0000004955 numeric UE units**; BSP sample error is zero. The [fixed read-only inspection](inspect-ue-landmarks.py) validates OBJ group/index/line provenance and writes only this evidence. Mesh asset hash is unchanged. These are representative surface correspondences, not measured actor pivots, full geometry/UV coverage, physical scale, or ten full-map landmarks.
- [Gameplay reference](../../References/gameplay-reference.md) now records the map's default-volume setup, four atrium blocking volumes, `MAXSTEPHEIGHT=35`, `MINFLOORZ=0.7`, and source-derived `TimeDilation=1.1` at `GameSpeed=1`. No effective native acceleration, runtime clearance, or trajectory result is inferred from these facts.

Owner questions remain pending: lock or revise the existing D-02 targets; select a physical scale reference (176 cm standing height would imply 2 cm/source unit, while existing numeric transport implies 88 cm at 1 cm/unit); and permit or reject the prepared isolated installed-executable launch. No selection is inferred from silence. P0/P1 gates remain open; collision, source textures/UVs, traversal, P2 art and P3 gameplay have not advanced.

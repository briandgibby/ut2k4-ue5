# Initial phase execution status

Updated: 2026-10-05. Scope: Rankin Visual Proof followed by the Rankin Combat Prototype.

The owner authorized execution and selected `C:\Users\brian\git-projects\ut2k4-ue5`. The three planning documents have moved to its `docs/` directory. This path is a Windows profile symlink to `C:\Users\Jack Thompson\git-projects\ut2k4-ue5`; both names address the same project. On 2026-10-04, the owner also authorized an initial commit/push to the private `briandgibby/ut2k4-ue5` repository. Repository exclusions are recorded in [README](../../README.md); the private local credential file and installed ReferenceGame copy are not staged.

## P0 evidence recorded

- [Reference copy record](reference-copy.json): 1,607 protected files were hashed before copying and verified byte-for-byte in `ReferenceGame/`.
- [Original preservation baseline](original-protected-files.csv): file paths, lengths, and SHA-256s. Saves, shader caches, logs, the secondary content folder, DirectX redistributables, and the old docs directory are outside the development copy; they remain untouched in the original installation.
- [Preservation recheck](original-preservation-check.json): all 1,607 protected original files still match; zero changed files after editor/export work.
- [Gameplay reference](../../References/gameplay-reference.md): 36 retained build-3369 scripts with hashes, source-derived contracts, native parameter readbacks, one jump viability probe and pending controlled trials.
- [Room reference](../../References/Rankin-reference.md): selected Flak atrium, source brush bounds/anchor, ten placement landmarks, locked scale-2 expectations and map-local/external dependencies.
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

The original-game smoke and corrected direct installed-executable reference route pass. Physical scale and D-02 targets are locked as recorded below; empirical P0 work remains open. Complete the walkthrough, controlled gameplay trials, landmark/route comparisons and scale-2 calibration checks. Resolve the paused-sampler timing discrepancy and obtain valid held-input/crouch evidence before accepting controlled comparisons. Rankin loads in the reference editor using `MAP LOAD FILE="..\Maps\DM-Rankin.ut2"`; its geometry exports with `MAP EXPORT FILE="..\..\Exports\Rankin\EditorRankin.obj"`. The earlier long absolute command was truncated by the editor command field. No source/prototype gameplay comparison or failed exporter has been described as passing.

P1 room acceptance and P2 visual work remain pending. Continue with the single Flak atrium and brace sample rather than expanding to a full-map converter.

## Continuation results — 2026-10-04

- [Original smoke](original-game-smoke.json): the installed executable reached its main menu and exited normally. [Capture](original-game-main-menu.png). All 1,607 protected hashes matched immediately before launch; original `UT2004.ini` and `User.ini` hashes are unchanged afterward. [Session preservation check](session-preservation-check.json) also checks all protected originals, four template assets, and the two saved atrium assets.
- [Copied-game launch](reference-game-launch.json): `ReferenceGame/System/UT2004.exe` displayed Steam **Application load error (0x02)** before engine startup. [Error capture](reference-game-launch-error.png). Removing the custom log argument did not resolve it. No Rankin game capture, actual FPS, movement trial, or weapon trial was produced. The precise internal Steam cause is not established.
- [Prepared fallback](reference-launch-fallback.json): use the installed executable with project-local `P0Runtime.ini`/`P0User.ini`, absolute ReferenceGame content/save/cache/music paths, and a project log. **Not executed.** It changes the requested copied-executable boundary and awaits the owner's decision. Native path/config overrides and loaded content must be verified before accepting a trial; recheck protected hashes afterward.
- [Saved UE surface samples](ue-landmark-samples.json): native `StaticMeshDescription` LOD0 readback found all four noncoplanar BSP points and one actual corner from each of ten landmark mesh groups under `(source X, -source Y, source Z)`, numeric scale 1. Maximum Euclidean coordinate error is **0.0000004955 numeric UE units**; BSP sample error is zero. The [fixed read-only inspection](inspect-ue-landmarks.py) validates OBJ group/index/line provenance and writes only this evidence. Mesh asset hash is unchanged. These are representative surface correspondences, not measured actor pivots, full geometry/UV coverage, physical scale, or ten full-map landmarks.
- [Gameplay reference](../../References/gameplay-reference.md) now records the map's default-volume setup, four atrium blocking volumes, `MAXSTEPHEIGHT=35`, `MINFLOORZ=0.7`, and source-derived `TimeDilation=1.1` at `GameSpeed=1`. No effective native acceleration, runtime clearance, or trajectory result is inferred from these facts.

These owner questions were pending at the 2026-10-04 handoff and resolved explicitly on 2026-10-05, as recorded below. P0/P1 gates remain open; collision, source textures/UVs, traversal, P2 art and P3 gameplay have not advanced.

## Repository snapshot and decision review — 2026-10-04

Initial snapshot [28892c6](https://github.com/briandgibby/ut2k4-ue5/commit/28892c6d7854a97e160ae700702b8bdc1cc08441) was pushed to the private repository's `main` branch. Git remote ref and GitHub API matched local HEAD. All 488 staged files matched their working bytes; the four protected template hashes and three retained transport artifact hashes matched. The five existing tests passed. Installed game/runtime configuration, credentials, logs, caches and backups remain local as described in [README](../../README.md).

The review package was proposed on 2026-10-04 and explicitly locked on 2026-10-05:

| Decision | Recommendation | Status / remaining evidence |
|---|---|---|
| Runtime boundary | Direct installed executable with private project INIs, absolute ReferenceGame paths and native ABSLOG | Authorized; corrected route verified after adding the existing CacheRecordPath override |
| Physical scale | 176 cm for the 88-source-unit standing collision height, `s=2 cm/unit` | Locked design correspondence; no contrary evidence for 1 cm/unit; retained transport remains scale 1 |
| D-02 | Fixed <=2 source units for sampled geometry position/dimension error; five movement trials at <=5%; three warmed native-1080p runs with P95 <=16.67 ms | Locked unless measured anomalies warrant reconsideration; required route/collision/weapon checks remain mandatory |

The superseded percentage formula permits 23.436587 units of atrium position error, or 46.873174 cm at scale 2. Fixed 2 units permits 4 cm. The fourteen measured points support sampled transport precision, not full-room dimensions/collision, and do not justify accepting unmeasured behavior.

## Decision-parameter checks — 2026-10-05

- [Runtime boundary verification](runtime-boundary-verification.json): direct installed executable, isolated native INI/userINI, twelve absolute content/save/cache/music/UCL paths and `ABSLOG` worked. Build 3369 and Rankin loaded. All 299 absolute linker paths are inside ReferenceGame; `Packages.md5` has an unqualified name, with identical protected baseline copies in both possible locations. Active F11 readback and two log markers witness isolated user configuration. Normal quit succeeded.
- The first authorized probe reached Rankin but exited after `GET Core.System Paths`; Windows recorded Core.dll `0xc0000409` then unknown-module `0xc0000005`. The causal mechanism is unproven. `LOG=absolute` did not create the requested log. The first launch changed `CacheRecords.ucl` and removed `OnslaughtBP.ucl`; [exact restoration](runtime-native-cache-restoration.json) preceded the corrected `Core.System.CacheRecordPath`/`ABSLOG` retry. The final check matches all **1,607 protected originals**, **four template assets** and **three retained transport artifacts**. Original INIs match; native/private [configuration changes](runtime-configuration-changes.json) are recorded separately. Temporary F8–F11 bindings were restored. Exact UCL baseline backups now reside privately in `ReferenceGame/P0ProtectedBaseline/`; working reference UCL files have normal runtime updates.
- [Default parameter readback](runtime-parameter-baseline.json): standing radius/half-height **25/44**, base eye **38**, GroundSpeed **440**, JumpZ **340**, AccelRate **2048**, AirControl **0.35**, active DefaultPhysicsVolume gravity **(0,0,-950)**, friction **8/0.3**, terminal velocity **2500**, GameSpeed **1**, TimeDilation **1.1**, zero bots, stock DMMutator with no successor/rule modifier, live FOV **90** and DoubleClickTime **0.25**. Difficulty **4** is the prepared match control, rather than the raw source default 1. At selected scale 2, standing height/radius are 176/50 cm; these are design calculations, not applied UE collision measurements.
- [One-jump viability check](runtime-jump-viability.json): one standing sample, five airborne samples and a delayed landing/control witness at fixed XY `(4724.301758,448)`, **outside the Flak atrium**. Native command-file execution works, and each state read has identical bracket timestamps with a non-null Pauser. Position/velocity energy estimates remain near gravity -950. Short paused intervals produce biased acceleration estimates from velocity/game-time differences; longer intervals reduce that discrepancy. Native tick cause and timing correction remain unresolved. No jump apex, duration, five-trial comparison or A/B result is accepted.
- The reversible `Toggle bDuck` binding did not yield an accepted crouched state. This is a failed input-control witness, not evidence that native crouching is broken. Source-derived crouch dimensions remain unmeasured. [Unpaused FPS witness](runtime-unpaused-fps.png) shows 458 current/368 native average FPS at 640×480; it is a snapshot, not a stable trial condition or UE packaged-performance result.
- Startup metadata discovery produced 102 missing-LevelSummary warnings, four TeamSymbols bounds errors and two team-symbol warnings. Their cause is unproven; no missing-StaticMesh warning was found. Preserve them as unresolved baseline anomalies.

No remaining owner choice blocks this bounded work. Next, resolve reference input/timing instrumentation and record the planned walkthrough and five controlled trials per action under documented conditions. P0/P1 stay open. After required P0 evidence passes, apply scale 2 in separate atrium P1 assets and check native UV/texture fidelity, collision and a source-equivalent character envelope; preserve the original transport proof.

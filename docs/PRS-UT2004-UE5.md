# UT2004 UE5 Remake — Product Requirements Specification

Status: Working draft v0.2 — P0 execution underway | Created: 2026-10-04

Companion documents: [PRD](PRD-UT2004-UE5.md) and [Phase Plan](PHASE-PLAN-UT2004-UE5.md).

At handoff, this specification must describe the implementation and identify remaining deviations.
The isolated UT2004 reference copy and source geometry exports exist. UE5 5.8.3 is installed; the native First Person project passed a qualitative Play in Editor smoke. The Flak atrium imported and reopened as a saved geometry inspection level. Physical calibration, a converted playable room, and UT gameplay implementation remain pending.

The original main-menu smoke now passes with unchanged protected hashes. Four noncoplanar BSP samples and ten landmark-group surface corners pass numeric saved-mesh correspondence; this does not accept actor pivots, physical scale or collision. Reference runtime trials are blocked by Steam load error `0x02` in the copied executable. A prepared installed-executable launch with isolated project INIs/paths awaits the owner's boundary decision. [Evidence/status](../Evidence/P0/status.md).

## 1. Introduction & scope

### 1.1 Document purpose

Specify the Rankin Visual Proof and Rankin Combat Prototype defined in the PRD.
Capability IDs C-01 through C-10 provide traceability. Phase IDs P0 through P5 match the Phase Plan.

### 1.2 Governing decisions

No ADRs exist. The owner authorized the initial phase scope and selected the project root on 2026-10-04.
The PRD §8 decision register holds D-01 through D-06 within the requested three-document set.
Sections below state intended behavior unless they explicitly label an observation.

| Category | Status |
|---|---|
| Observed | Original game is build 3369. UnrealEd and UCC exist. DM-Rankin is installed. |
| Observed | Reference PC: Windows 11, i5-12400F, 32 GB RAM, RTX 4060 Ti 16 GB. |
| Observed | UE5 5.8.3 is installed at `F:\Program Files\Epic Games\UE_5.8`; build changelist 58210709. |
| Proposed | Separate UE5 project, one recovered room first, full Rankin later, offline practice release. |
| Measured | Source exports and fixed Blender/FBX probes succeeded. The atrium's UE5 numeric bounds import and saved-asset reload succeeded; physical scale and per-corner UE UV fidelity remain unverified. |
| Installed | UE5 5.8.3, source tools build 3369, and Blender 5.2.2 LTS. Native Blueprint First Person template passed a qualitative Play in Editor smoke. |
| Deferred | Physical scale/landmark calibration, final numeric tolerances, UT implementation language split, and external distribution scope. |

### 1.3 Exclusions

The first prototype excludes bots, network sessions, vehicles, additional weapons/maps, and full-game progression or menus. [C-10]
It will not modify the original renderer or provide a general conversion framework. [C-09, C-10]

### 1.4 Conventions and integrity

- Record a value with its source, units, and status: observed, source-derived, proposed, or measured. [C-01, C-07]
- Source code values are comparison references. They are not proof that identical UE5 values produce identical behavior. [C-04, C-05]
- Source units mean build-3369 world units. UE5 lengths use centimeters after P0 calibration. [C-02, C-04]
- A phase gate passes only after its evidence exists. A document or screenshot alone does not prove gameplay or runtime performance. [C-07, C-10]

## 2. System architecture overview

### 2.1 Working boundaries

The original installation remains the source reference. A separate reference copy supplies UnrealEd baseline runs and exports. [C-01, C-09]
Selected development root: `C:\Users\brian\git-projects\ut2k4-ue5`. The owner supplied this location and authorized initial execution. [C-09]

| Location | Responsibility | Capabilities |
|---|---|---|
| `ReferenceGame/` | Development reference copy of UT2004, editor runs, and original behavior captures | C-01, C-04, C-05, C-09 |
| `References/` | Source links, asset manifest, reference contracts, and baseline measurements | C-01, C-02, C-04, C-05 |
| `Exports/` | Exported art and intermediate geometry, separate from original packages | C-01, C-02, C-03 |
| `Prototype/UT2004UE5.uproject` | Native Blueprint First Person project and separate atrium inspection level | C-02 through C-08 |
| `Evidence/P0/` through `Evidence/P5/` | Captures, trial results, frame-time CSVs, and gate decisions | C-07, C-10 |
| `Builds/RankinCombatPrototype/` | Packaged Windows evaluation build | C-08 |

Reference, export, and evidence directories are being populated during P0. The native prototype exists; Builds remains planned.

### 2.2 Engine and gameplay approach

Create the basic project in P0 using UE5's native First Person template without its Arena Shooter enemy variant. Use it for P1 room recovery. [C-02, C-06]
Use native level, character, input, material, projectile, UI, and packaging systems. [C-02 through C-08]
Do not add a third-party gameplay framework or multiplayer service to the prototype. [C-10]

P1–P2 use a basic walking character to inspect conversion and graphics. P3 introduces the UT2004 movement and weapon contract. [C-02, C-04, C-05]
P3 selects Blueprint/C++ responsibilities after the reference trials exist. A custom movement component requires a demonstrated fidelity limitation. [C-04]
The developer records the selected class/asset paths in this document before handing P3 work to another implementer. [C-01, C-04, C-05]

Observed P0 assets are `/Game/FirstPerson/Lvl_FirstPerson` and `/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter`, `BP_FirstPersonGameMode`, and `BP_FirstPersonPlayerController`. Input contexts are `/Game/Input/IMC_Default` and `/Game/Input/IMC_MouseLook`. Creation used Blueprint, Variant None, Desktop, and Maximum. The stock capsule is approximately radius 34 cm and half-height 96 cm; it is not a calibrated equivalent of UT2004's radius 25 and half-height 44 source units. [Template evidence](../Evidence/P0/ue-project-setup.json) records the limited smoke check. [C-02, C-04]

The separate `/Game/RankinRecovery/L_FlakAtrium_Transport` level contains one combined `/Game/RankinRecovery/SM_FlakAtrium_Transport` mesh at the origin with collision disabled. It is a P1 transport probe, not an accepted walking level or actor reconstruction. The native template assets remain unchanged. [C-01, C-02]

### 2.3 Rendering approach

Use Lumen as the initial global-illumination and reflection candidate. Recreate selected surfaces as UE5 materials with authored surface response. [C-03]
P2 compares the result with the original's color, silhouette, and navigation cues. [C-02, C-03]
Old textures and geometry do not become detailed PBR content solely through import or Nanite. [C-03]
Enable further rendering features only when the P2/P4 visual and frame-time results justify them. [C-03, C-07]

## 3. Data model

These records are files and game state, not a service database.

| Record | Required fields | Authority / coverage |
|---|---|---|
| Asset manifest row | Asset ID, source package/object, source hash, asset type, tool/version, export path, UE5 asset path, conversion notes, reuse status | `References/asset-manifest.csv` [C-01] |
| Map reference | Source build/map hash, selected room, anchor transform, scale factor, landmarks, surface references, route list, interactive geometry inventory | `References/Rankin-reference.md` [C-02] |
| Gameplay reference | Class/file, parameter or rule, units, source value, captured behavior, trial conditions, accepted tolerance | `References/gameplay-reference.md` [C-04, C-05] |
| Capture record | Phase, engine version, project revision/snapshot, map, camera or input sequence, preset, resolution, hardware, result files | Phase evidence directory [C-03, C-07] |
| Gate decision | Phase, evidence links, pass/fail, unresolved gaps, decision owner, selected next scope | Phase evidence directory and PRD decision register [C-10] |
| Practice state | Player transform, health, ammunition, target health, active projectiles, firing timers, movement state | Runtime UE5 state [C-05, C-06] |

The manifest resolves every dependency in the evaluated build, including map-local assets and generated replacements. [C-01]
Use ordinary CSV and Markdown records. P1 must not build an asset database or converter service. [C-01, C-10]

## 4. Core engines / state machines

### 4.1 Content recovery lifecycle

An asset progresses through `identified → exported → imported → compared → accepted`. [C-01, C-02]
A failed step retains the source reference, error, and current artifact. It does not become accepted by substituting an unlabeled placeholder. [C-01, C-02]
An intentional replacement records the affected source object and owner decision. [C-01, C-03]

P1 tests a representative room's brushes, prop placement, material alignment, scale, and collision. [C-02]
The pipeline must recover actors and brushes separately from the meshes and texture pixels they reference. [C-01, C-02]

### 4.2 Movement contract

Reproduce walking, strafing, jump, double jump, dodge, dodge jump, and wall dodge under the reference game's permitted conditions. [C-04]
The double jump is not a generic extra jump at any point in the trajectory. Its reference rule includes an apex velocity window. [C-04]
Wall dodge requires the reference wall-contact and movement conditions. The source class also distinguishes walking from falling dodge behavior. [C-04]

Verified `xPawn` defaults and local configuration provide the following starting references:

| Reference field | Source value | Units / meaning |
|---|---:|---|
| GroundSpeed / AirSpeed | 440 / 440 | Source units per second |
| AccelRate | 2048 | Source acceleration parameter |
| AirControl | 0.35 | Source parameter, not an automatic UE5 equivalent |
| JumpZ | 340 | Source vertical velocity |
| DodgeSpeedFactor / DodgeSpeedZ | 1.5 / 210 | Factor and source vertical velocity |
| MaxMultiJump / MultiJumpBoost | 1 / 25 | Extra-jump count and velocity boost |
| Double-jump apex condition | Absolute vertical velocity below 100 | Source units per second, plus source state/count conditions |
| DoubleClickTime | 0.25 | Seconds, observed local `User.ini` |
| DefaultFOV / DesiredFOV | 90 / 90 | Observed local camera settings |

The source-derived values come from `XGame/Classes/xPawn.uc` in the inspected 3369 archive and the corresponding [script reference](https://github.com/Deaod/UT2004/blob/master/XGame/xPawn.uc).
Record gravity, collision dimensions, floor rules, camera behavior, and inherited settings in P0 before implementing the comparison trials. [C-02, C-04]

### 4.3 Shock Rifle contract

Primary fire traces a beam. Secondary fire creates a moving core. A qualifying beam hit on a core triggers the combo explosion. [C-05]
The core must produce one explosion and be removed. Ordinary wall impact and combo impact remain distinct events. [C-05]
Ammo accounting includes the primary shot, secondary shot, and combo-specific consumption. P0 captures the complete sequence. [C-05]

| Reference class / field | Verified value | Meaning |
|---|---:|---|
| ShockBeamFire damage / FireRate | 45 / 0.7 | Base damage and seconds between primary shots |
| ShockProjFire FireRate / AmmoPerFire | 0.6 / 1 | Seconds between secondary shots and shot ammunition |
| ShockProjectile Speed / MaxSpeed | 1150 / 1150 | Source units per second |
| ShockProjectile Damage / DamageRadius | 45 / 150 | Ordinary explosion base damage and source radius |
| ShockProjectile ComboDamage / ComboRadius | 200 / 275 | Combo base damage and source radius |
| ShockProjectile ComboAmmoCost | 3 | Combo-specific consumption parameter |
| ShockProjectile LifeSpan | 10 | Seconds |
| ShockAmmo InitialAmount / MaxAmmo | 20 / 50 | Initial and maximum ammo |

Source: [3369 archive mirror](https://unrealmassdestruction.com/downloads/ut2004scripts3369.zip), `XWeapons/Classes/`.
Its inspected entries include the rifle, fire modes, projectile, and ammunition classes.

Use source rules and reference trials for falloff, obstruction, momentum, ownership, and ammo handling at low ammunition. [C-05]
These states occur during normal firing. P3 verifies them without implementing unrelated weapons or full armor/adrenaline systems. [C-05, C-10]

### 4.4 Offline practice lifecycle

The practice loop uses `loading → active → player-dead → reset → active`. A manual reset also works from `active`. [C-06]
Start with the documented player spawn, 100 health, 20 Shock Rifle ammunition, and stationary targets with 100 health. [C-05, C-06]
These health values define prototype fixtures. P0 records the original player-health reference separately. [C-06]
Place target fixtures without changing the source traversal layout. Record their positions in the practice reference. [C-02, C-06]

Reset restores the player, targets, ammunition, health, firing timers, and movement state. Remove projectiles from the previous run. [C-06]
Out-of-world death exposes the reset action. The prototype does not require a match, opponent AI, or a complete damage economy. [C-06, C-10]

## 5. Integration adapters

No runtime service adapters are required. The following seams are development-time file workflows.

| Seam | Input → output | Failure posture | Capabilities |
|---|---|---|---|
| Reference editor / UCC | Original map in the reference copy → actor/brush T3D, native static-mesh triangles, and loaded-editor OBJ geometry | Retain the untouched source. UCC Level OBJ fails; loaded-editor OBJ succeeds. Map-local triangle batch export remains partial. | C-01, C-02, C-09 |
| UModel | Supported UE2 packages → meshes, textures, and selected animations | Verify actual object support. Do not treat extracted assets as a reconstructed map. | C-01, C-02, C-03 |
| Blender | Native brace triangles and loaded-editor OBJ → checked brace FBX and fixed atrium geometry FBX | Geometry/UV checks pass. Four room FBX material labels are abbreviated and recorded; original shading/collision and UE5 scale remain unverified. | C-01, C-02, C-03 |
| UE5 import | Fixed atrium FBX → one native combined inspection mesh and separate level | Built-in Editor Python and legacy FbxFactory; scene-unit conversion and generated collision disabled. Numeric bounds passed; physical scale, per-corner UVs, source shading/materials, and collision remain unverified. | C-01, C-02, C-03 |
| Gameplay references | Public scripts and controlled original trials → documented behavior contract | Record gaps in native/inherited behavior and measure them in the reference copy. | C-04, C-05 |

Pin the exact tool versions after P0/P1 compatibility checks. [C-01]
The current fixed-prop seam uses UCC 3369 and Blender 5.2.2 LTS. [P0 status](../Evidence/P0/status.md) records the tests, artifacts, failures, and pending gate checks. [C-01, C-02]

The [fixed UE importer](../Tools/import_rankin_room_ue.py) verifies the passing Blender report and FBX hash before importing. [Import evidence](../Evidence/P1/ue-import/validation.json) measures outer bounds consistent with `UE XYZ = (source X, -source Y, source Z)` and numeric dimension ratios `(1,1,1)`. [Fresh-editor evidence](../Evidence/P1/ue-import/serialized-inspection.json) repeats those saved-mesh measurements. This provisional transport does not replace §7.1 calibration. UE reports 9,392 render triangles, one UV channel, and 66 grid-material slots. The eight-triangle difference from 9,400 source triangulation candidates is consistent with the eight source zero-area triangles, but their omission has not been individually traced. [C-01, C-02]
UT4X explicitly excludes UE5 support. UnrealPort and old T3D importers are research leads, not a committed automatic pipeline. [C-02]
Adding a converter framework or dependency requires explaining why the current room workflow cannot meet C-02. [C-02, C-10]

## 6. Surface / view specifications

### 6.1 First-person view

Show the recreated map, crosshair, and Shock Rifle presentation. Match the reference camera for fidelity captures. [C-02, C-03, C-05]
Keep required routes and practice targets visible under the chosen visual preset. [C-02, C-03, C-06]

### 6.2 Practice HUD and reset

Display player health, ammunition, a crosshair, and target hit/death feedback. [C-05, C-06]
Expose a reset action in the active and dead states. Document the selected binding in the build's controls note. [C-06, C-08]
The HUD does not display package paths, exporter details, or source hashes. Developer evidence stores those records. [C-01, C-06]

### 6.3 Evaluation evidence

Capture matching viewpoints for original and prototype lighting, material response, reflections, and shadows. [C-03]
Record camera transform/FOV and settings beside each capture. [C-02, C-03]
P2 uses a nonfunctional preview of the intended target fixture for readability review. P3 adds its combat behavior. [C-03, C-06]
Store developer measurements outside the player-facing HUD. [C-07]

## 7. Calculation specifications

The following tolerances are proposed and become gate criteria when P0 resolves D-02.

### 7.1 Geometry and scale [C-02]

Observed bounded readback: [fourteen source/UE samples](../Evidence/P0/ue-landmark-samples.json) match `(X,-Y,Z)` at numeric scale 1, maximum error `0.0000004955`. This is a mesh-source precision check, not a locked D-02 tolerance or physical calibration. Physical scale remains an owner-selected reference correspondence; no rescale is applied.

Calibrate one source-to-UE5 transform using a fixed anchor, axis mapping, and scale factor `s`.
Convert UE5 landmark coordinates back to the source frame before comparing them.
For each sampled room, let `L` be the source room's diagonal length.
Proposed positional tolerance: `max(2 source units, 0.01 × L)`.
Proposed dimensional tolerance: `max(2 source units, 0.01 × reference dimension)`.
Measure at least 10 fixed landmarks across the full-map release. Check every required route for collision and clearance.
An unmeasured landmark or blocked required route fails acceptance.

### 7.2 Movement [C-04]

Use five successful controlled reference trials per action, with the same input schedule and matched frame-rate conditions.
For a nonzero reference quantity, error is `abs(prototype − reference) / abs(reference)`.
Compare distance, apex height, and action duration where each applies. Proposed maximum error is 5% per measured quantity.
Convert UE5 distances and velocities into the calibrated source units first.
Forbidden reference actions must remain forbidden. A zero reference displacement uses the locked positional tolerance, not division by zero.

### 7.3 Damage and ammunition [C-05, C-06]

Target health after an accepted damage event is `max(0, previous health − applied damage)`.
Applied damage must follow the reference falloff and obstruction behavior, rather than always equal the base-damage table.
Ammunition reflects each accepted source-equivalent consumption event. Rejected firing does not create a projectile or damage event.
The initial ammo is 20 and the maximum is 50 for the prototype's Shock Rifle.
Record the observed complete combo sequence before asserting its total ammo cost.

### 7.4 Performance [C-07]

Measure a packaged Development build outside the editor at 1920×1080 native resolution.
Disable dynamic resolution, frame generation, VSync, and frame caps for the acceptance capture.
Record the exact preset and Lumen mode. Use a fixed 90-second route after a 30-second warm-up.
Run the route three times and record frame-time data for every run.
Compute P95 using the nearest-rank method: sort frame times and select rank `ceil(0.95 × frame count)`.
Proposed acceptance: each run has P95 frame time ≤16.67 ms.
Also report median frame time, maximum frame time, and counts above 33.33 ms and 50 ms.
Cold-start shader/asset preparation is reported separately and must not be hidden inside the warm-run result.

### 7.5 Coverage [C-01, C-10]

Manifest coverage is `recorded delivered dependencies / total delivered dependencies`.
Acceptance requires coverage of 1.0. A missing source/reuse record is incomplete coverage.
Gate records distinguish passing tests, failed tests, and unexecuted tests.

## 8. Configuration & console

| Setting | Proposed default / reference | Authority | Capabilities |
|---|---|---|---|
| Map | DM-Rankin recreation | PRD D-02 and project map asset | C-02, C-06 |
| Camera comparison | Observed original FOV 90, with matching capture transform | Reference capture record | C-02, C-03 |
| Dodge input window | 0.25 seconds | Observed local configuration; runtime trials pending | C-04 |
| Practice state | Player/target health 100, ammo 20, defined spawn | Practice fixture record | C-05, C-06 |
| Visual preset | Initial Lumen candidate, exact quality settings selected in P2 | Native project/render settings and capture record | C-03, C-07 |
| Performance capture | Native 1920×1080, uncapped warmed route | §7.4 | C-07 |
| Engine/tool versions | Exact versions selected and recorded during P0/P1 | Project association and tool manifest | C-01, C-08 |

Use native project settings and level assets. Do not create a separate configuration service. [C-10]
The acceptance preset is reproducible. Changing it requires a new labeled capture. [C-07]
Developer console/profiling facilities are available in the evaluation build and are not a required player workflow. [C-07, C-08]

## 9. Security & access model

The prototype runs locally under the user's Windows account. It has no login, cloud account, tenant model, or online session. [C-08, C-10]
Development tools read original content and write only to the selected development root. [C-09]
Compare protected-file hashes before each original-game smoke launch. Record configuration changes produced by that normal launch separately; only those documented changes may update the next configuration baseline. Unexplained changes fail C-09. [C-09]
Do not copy CD keys, account tokens, or identifying multiplayer logs into manifests, captures, or packaged content. [C-01, C-09]

Record whether each asset is original, converted, newly authored, or replaced, and its reuse status. [C-01]
Local evaluation does not mark an asset as cleared for external distribution. Resolve D-05 before releasing an external package. [C-01, C-10]
This is a release condition, not a finding that a particular asset license permits or forbids reuse.

## 10. Deployment topology

| Milestone | Executable topology | Acceptance evidence | Capabilities |
|---|---|---|---|
| P1 | Local UE5 editor and one recovered room | Import, layout, and collision results | C-01, C-02 |
| P2 | Local UE5 editor plus an early packaged Windows Development build | Visual review and packaged room performance gate | C-02, C-03, C-07 |
| P3–P4 | Local playable UE5 project plus packaged Windows Development builds | Movement/weapon trials outside the editor, complete Rankin traversal, and packaged performance gates | C-02, C-04, C-05, C-06, C-07 |
| P5 | Packaged local Windows Development build | Three launches, practice loop, packaged performance captures, original preservation check | C-07, C-08, C-09 |
| Future expansion | Topology selected by D-06 | New capability scope and verification gate before implementation | C-10 |

A successful editor session does not satisfy C-08. The packaged application must run without the editor process. [C-08]
Record build identity, engine version, runtime prerequisites, controls, and known deviations with the evaluation package. [C-01, C-08]
No installer, server, launcher replacement, updater, or public hosting is required for P5. [C-08, C-10]

### Reference index

- [Epic UE2 sitemap](https://docs.unrealengine.com/udk/Two/SiteMap.html), [BSP](https://docs.unrealengine.com/udk/Two/BspBrushesTutorial.html), [static meshes](https://docs.unrealengine.com/udk/Two/StaticMeshesTutorial.html), and [materials](https://docs.unrealengine.com/udk/Two/MaterialTutorial.html).
- [3D Buzz UT2003/2004 training](https://archive.org/details/3DBuzz).
- [T3D format](https://unrealarchive.org/wikis/unreal-wiki/Legacy:T3D_File.html).
- [UModel](https://www.gildor.org/en/projects/umodel) and [Blender PSK/PSA importer](https://github.com/DarklightGames/io_scene_psk_psa).
- [3369 script dump](https://github.com/Deaod/UT2004) and [inspected archive mirror](https://unrealmassdestruction.com/downloads/ut2004scripts3369.zip).
- [UE5 First Person template](https://dev.epicgames.com/documentation/en-us/unreal-engine/first-person-template-in-unreal-engine).
- [UE5 hardware requirements](https://dev.epicgames.com/documentation/en-us/unreal-engine/hardware-and-software-specifications-for-unreal-engine) and [Lumen details](https://dev.epicgames.com/documentation/en-us/unreal-engine/lumen-technical-details-in-unreal-engine).
- [UT4X-Converter](https://github.com/xtremexp/UT4X-Converter) and [UnrealPort](https://github.com/Thor110/UnrealPort), with their documented limits.

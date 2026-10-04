# UT2004 UE5 session continuity

Last updated: 2026-10-04. Read this first when continuing the project. Keep it current at each session handoff: record completed work, evidence, unresolved decisions, and the next bounded task. Verify mutable paths, running processes, and artifact state before relying on this snapshot.

## Goal and boundaries

Build a local UE5 remake prototype: first a Rankin Visual Proof, then the Rankin Combat Prototype with UT2004 movement, Shock Rifle, stationary practice targets, HUD, and offline reset. The owner authorized beginning the initial phases. P0 reference work is underway; bounded P1 recovery feasibility has progressed, but neither phase gate has passed.

- Work in `C:\Users\brian\git-projects\ut2k4-ue5`. The `brian` profile path is a symlink to `C:\Users\Jack Thompson`; both paths address the same project. Prefer the owner-supplied `brian` path in documentation.
- The original installation is `F:\Program Files\steamapps\common\Unreal Tournament 2004`. Development editor/export work uses `ReferenceGame/` inside the project root.
- Follow the owner's minimal-change policy: extend existing patterns, use the smallest correct change, and avoid unrelated cleanup or speculative abstractions. Explain why the smaller approach is insufficient and obtain approval before materially expanding modules, adding dependencies, or introducing a new public abstraction.
- The owner authorized an initial commit/push on 2026-10-04 to the private repository `https://github.com/briandgibby/ut2k4-ue5`. Local branch `main` and `origin` now exist; verify the pushed commit before relying on the remote. No PR, converter framework, multiplayer, extra weapons/maps, or full-map implementation has been created.
- Installation and sign-in are complete. Use the installed tools; no engine installation confirmation is pending.
- Preserve originals and the stock template. Keep source-derived, measured, proposed, failed, and unexecuted results distinct. Public distribution remains outside the local evaluation scope.

## Read these records

| File | Purpose |
|---|---|
| [P0 status](Evidence/P0/status.md) | Current execution summary, successes, failures, and open gates |
| [PRD](docs/PRD-UT2004-UE5.md) | Product scope, proposed targets, and D-01 through D-06 decisions |
| [PRS](docs/PRS-UT2004-UE5.md) | Requirements, actual asset locations, calibration, and acceptance methods |
| [Phase plan](docs/PHASE-PLAN-UT2004-UE5.md) | Work packages and P0–P5 dependencies |
| [Rankin reference](References/Rankin-reference.md) | Flak atrium bounds, source landmarks, dependencies, and recovery procedure |
| [Gameplay reference](References/gameplay-reference.md) | Inspected build-3369 script contracts and unexecuted runtime trials |
| [Asset manifest](References/asset-manifest.csv) | Four initial export/probe provenance rows; not full dependency coverage |
| [New-session prompt](docs/NEXT_SESSION_PROMPT.md) | Copyable instructions to resume work |

The PRS reference index also retains the earlier UT2004 modding research, including the archived 3D Buzz training and UE2 documentation. Reuse it rather than restarting the research spike.

## Installed tools and native project

| Tool | Verified version and location |
|---|---|
| UT2004 / UnrealEd / UCC | Build 3369; development tools in `ReferenceGame/System/` |
| Unreal Engine | 5.8.3, changelist 58210709; `F:\Program Files\Epic Games\UE_5.8` |
| UE editor | `F:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe` |
| UE commandlet | Same directory, `UnrealEditor-Cmd.exe` |
| Blender | 5.2.2 LTS; `C:\Users\Jack Thompson\AppData\Local\Programs\blender-5.2.2-windows-x64\blender.exe` |
| Project | [Prototype/UT2004UE5.uproject](Prototype/UT2004UE5.uproject) |

The native project was created through the UE project browser: Blueprint First Person, Variant None, Desktop, Maximum. The built-in PythonScriptPlugin is enabled for Editor targets only. There is no external Python plugin or gameplay framework.

The stock level is `/Game/FirstPerson/Lvl_FirstPerson`. Blueprint assets are `/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter`, `BP_FirstPersonGameMode`, and `BP_FirstPersonPlayerController`; input contexts are `/Game/Input/IMC_Default` and `/Game/Input/IMC_MouseLook`.

Play in Editor smoke observed spawn, mouse look, jump camera response, and return to the editor. This was qualitative; walking distance, trajectory, UT fidelity, packaged execution, and performance were not accepted. Initial shader/PSO compilation took several minutes and is not a warm-run performance result. [Setup evidence](Evidence/P0/ue-project-setup.json) records four protected template file hashes, all unchanged after import.

At the previous handoff, UE Editor was left open on the atrium inspection level in Unlit mode; the reference UnrealEd had also been used. Rediscover running processes/windows rather than reusing old IDs. Close the relevant project before commandlet reimport. The editor may open the stock map on a normal project launch; select the inspection level explicitly. Its Lit view is dark because the probe contains no lights.

## Completed recovery and its limits

1. A separate reference copy was verified against 1,607 protected original files. The latest [preservation recheck](Evidence/P0/original-preservation-check.json) reports zero changes. [Baseline CSV](Evidence/P0/original-protected-files.csv) contains paths, sizes, and SHA-256s.
2. Native UCC Level T3D exported Rankin: 1,949 actors and 3,243 brush polygons in [myLevel.t3d](Exports/Rankin/myLevel.t3d). HumanoidHardware StaticMesh T3D exported 135 objects. Map-local mesh batch export is partial: 25 files, then a `houreceilingpanel` file-open failure.
3. UCC Level OBJ failed with a native exporter fault. The loaded reference editor succeeded instead: [EditorRankin.obj](Exports/Rankin/EditorRankin.obj), compiled BSP plus 729 actor-mesh groups. These include all 664 StaticMeshActors and four movers, but do not recover mover behavior.
4. [Brace01HA probe](Tools/rankin_prop_probe.py) passed saved-Blender and FBX position/UV/triangle/material-label checks. Its five [standard-library tests](Tests/test_rankin_prop_probe.py) passed. Original normals, collision, appearance, and independent UE prop/pivot checks remain open.
5. [Fixed room probe](Tools/rankin_room_probe.py) clips BSP to the Flak atrium and retains 45 intersecting actor meshes whole. It produces 46 groups, 9,202 faces, and 27,804 UV corners. Blender/FBX corner positions, UVs, and polygon material assignments passed. Four FBX labels are abbreviated; eight source zero-area triangles are recorded. Crossing props extend beyond the room box. See [room validation](Evidence/P1/room-probe/validation.json).
6. [Fixed UE importer](Tools/import_rankin_room_ue.py) imported one combined mesh through native Editor Python and legacy `FbxFactory`. It verifies the upstream pass flag and FBX hash first. The successful commandlet exited 0 with two near-zero tangent/binormal warnings. A first failed actor-spawn attempt is retained; spawning the native StaticMeshActor class resolved it.

Native UE assets:

- Mesh: `/Game/RankinRecovery/SM_FlakAtrium_Transport`.
- Level: `/Game/RankinRecovery/L_FlakAtrium_Transport`.
- One mesh actor at origin, zero rotation, scale 1. Collision is explicitly disabled. No source materials or textures were imported.
- Saved bounds: min `(445.5229187,1375.4136963,-552)`, max `(1962.4521484,2776.0627441,1024)`.
- LOD0: 20,703 render vertices, 9,392 triangles, one UV channel, 66 sections/material slots. All slots use `WorldGridMaterial`.
- [Import report](Evidence/P1/ue-import/validation.json) and [fresh-editor inspection](Evidence/P1/ue-import/serialized-inspection.json) agree on those measurements. The later inspection closes the import-time report's pending reload check.
- [Native UE unlit capture](Evidence/P1/ue-import/FlakAtrium-UE5-unlit.png) shows floor, openings, braces, and ledges. It is geometry inspection, not the P2 visual proof or a matched original capture.

Coordinate facts: raw native OBJ is `(source X, source Z, source Y)`. The Blender room restores source XYZ by swapping Y/Z and reversing winding. UE outer bounds are consistent with `(source X, -source Y, source Z)`, with dimension ratios `(1,1,1)`. This is provisional numeric transport, not physical calibration or per-vertex/landmark proof. Source triangulation has 9,400 candidates; eight fewer UE triangles are consistent with the known zero-area triangles, but individual omissions have not been traced. One UE UV channel does not establish UV-value fidelity.

The Flak atrium's nominal BSP box is source min `(768,-2720,-512)`, max `(1920,-1376,1024)`; floor anchor `(1344,-2048,-512)`. Its ten recorded landmarks are actor origins, not measured surfaces or completed full-map runtime comparisons. The stock UE capsule (approximately radius 34 cm, half-height 96 cm) is not a calibrated equivalent of UT2004's radius 25 and half-height 44 source units.

UModel was not acquired; its linked Win32 download returned 404. The current bounded workflow does not need another extraction tool for geometry. Do not repeat the failed UCC OBJ route or build a general converter without a demonstrated need and revised scope. Recovery commands are in the Rankin reference. The fixed UE importer overwrites its inspection mesh/level when rerun; do not use it to overwrite later accepted work.

## Next session sequence

Latest continuation evidence (2026-10-04): [original-game smoke](Evidence/P0/original-game-smoke.json) reached the main menu and exited normally, with no original INI changes. [Session preservation](Evidence/P0/session-preservation-check.json) rechecks all 1,607 protected originals, four template assets and both saved atrium assets. [Native landmark samples](Evidence/P0/ue-landmark-samples.json) verify four noncoplanar BSP points plus ten actual landmark-group corners at numeric `(X,-Y,Z)`, scale 1; maximum error `0.0000004955`. This adds representative surface evidence, not physical scale/pivot/UV/collision acceptance. The fixed read-only script is `Evidence/P0/inspect-ue-landmarks.py`.

Runtime blocker: the copied `ReferenceGame/System/UT2004.exe` displays Steam `Application load error (0x02)` before engine startup. Both launch attempts and the screenshot are recorded in [reference-game-launch.json](Evidence/P0/reference-game-launch.json). The existing reference UnrealEd and UE editor were reused, and remain open; no reimport was performed. No reference gameplay trials or actual FPS were measured.

Owner questions were presented but remain unanswered: existing D-02 targets versus revised geometry tolerance; physical standing-cylinder correspondence (176 cm implies 2 cm/source unit; current numeric transport implies 88 cm at 1 cm/unit); and permission to test the installed executable with project-only runtime INIs and absolute ReferenceGame paths. [Fallback command](Evidence/P0/reference-launch-fallback.json) and `ReferenceGame/System/P0Runtime.ini`/`P0User.ini` are prepared, **not executed**. Do not treat elapsed time as approval. Confirm engine override behavior/content paths before accepting this route and recheck protected hashes after any authorized launch.

The gameplay reference now corrects source step/floor constants (`35`, `0.7`) and records Rankin's default volume, four atrium blocking volumes and `TimeDilation=1.1` at normal `GameSpeed=1`. Effective native trajectory/clearance remain unmeasured. P0 and P1 are still open.

Repository snapshot: records/tooling/tests, the native UE project/content, retained script references, source geometry exports, checked Blender/FBX handoffs and measured evidence are included. The local ReferenceGame installation, credentials, editor/runtime logs, generated caches/builds and Blender backups remain untracked; [README](README.md) records the boundary. `.gitattributes` preserves exact stored bytes. All five existing standard-library tests passed before the initial commit. Commit/push authorization does not lock gameplay/scale targets or authorize a runtime-boundary change by itself.

1. Start in the project root, read the records above, and inspect current artifacts/processes. Reuse the verified exports and installed native project.
2. Resolve the copied-runtime launch blocker within the owner's approved boundary. The original menu smoke is already recorded; check protected hashes before any further installed-executable launch and record runtime configuration changes separately. Obtain the Rankin walkthrough, matching camera views, required routes and interactive geometry inventory with verified isolated reference paths.
3. Run the controlled movement and Shock Rifle trials listed in the gameplay reference. Record actual frame rate, inputs, effective gravity/collision, match options, modifiers, and fixture conditions. All existing gameplay values are source contracts; no runtime trials have been measured.
4. Calibrate physical source-to-UE scale and individual landmarks. Resolve D-02 with the owner where needed: geometry/gameplay tolerances and the 1080p performance target are still proposed. Record the P0 gate outcome; do not silently accept proposed values.
5. Once required P0 evidence/decisions are resolved, continue the same atrium's P1 collision, source texture/material mapping, UE UV checks, landmark dimensions, and basic-character traversal. Preserve the transport proof and stock template, and document bounded repairs and repeatability.

P2 art/lighting, P3 UT movement and Shock Rifle implementation, full Rankin reconstruction, packaging, and expansion remain future gated work. No phase is accepted by a screenshot or a source-value table alone. Update the existing status, manifest, planning documents when decisions change, and this continuity file before handing off.

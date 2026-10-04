# UT2004 UE5 Remake — Phase Plan

Status: Working draft v0.2 | Created: 2026-10-04 | Execution: P0 in progress

Requirements: [PRD](PRD-UT2004-UE5.md) and [PRS](PRS-UT2004-UE5.md).

Goal: deliver the Rankin Combat Prototype after proving one-room recovery, visual value, and gameplay fidelity.
This is a phase and work-package plan. Detailed code tasks follow only after the relevant phase decisions resolve.
The owner authorized initial phase execution on 2026-10-04 and selected the project root. Public release and a full-game commitment remain outside this scope.

## Global constraints

- First release: DM-Rankin, UT2004 movement, Shock Rifle, stationary practice targets, HUD, and offline reset.
- Preserve the original build-3369 installation. Run development editor/export work on a separate reference copy.
- Compare protected-file hashes before original-game smoke launches. Record normal launch-generated configuration changes separately and update the configuration baseline only from those documented changes.
- Use the native UE5 framework. Do not add a gameplay framework, backend, general converter, or multiplayer service to the prototype.
- Mark proposed targets and unexecuted checks. Do not present research, source values, or editor previews as measured acceptance.
- Each phase ends with a pass/fail record and a decision about the next bounded scope.
- Extra dependencies or broader reconstruction require evidence that the smaller approach cannot satisfy the phase requirements.
- There are no calendar or cost commitments. Estimate remaining work after P1–P3 evidence exists.
- Execute the first phases in the supplied project root. The owner authorized commit/push to the private `briandgibby/ut2k4-ue5` repository on 2026-10-04. Do not create ADR files or a separate backlog.

## Delivery sequence and gates

`P0 reference → P1 room recovery → P2 visual payoff → P3 playable room → P4 full Rankin → P5 packaged evaluation`

| Phase | Deliverable | Depends on | Gate decision |
|---|---|---|---|
| P0 | Baselines and locked pilot decisions | Planning scope review | Can comparisons and source handling be defined? |
| P1 | Recovered navigable room | P0 | Can the room be reconstructed with a repeatable bounded workflow? |
| P2 | Rankin Visual Proof | P1 | Does the visual result justify gameplay work? |
| P3 | Playable room | P2 | Can the selected movement and weapon contract be reproduced? |
| P4 | Full playable Rankin | P3 and a measured completion estimate | Does the room workflow scale across the map? |
| P5 | Rankin Combat Prototype | P4 | Expand, revise the prototype, or stop? |

A failed gate produces an evidence record. It does not silently move work into the next phase.
The owner can authorize a bounded correction and repeat the affected check.
If scope or targets change, update all three documents before dependent work continues.

## P0 — Establish the reference and project boundary

**Coverage:** C-01, C-02, C-04, C-05, C-07, C-09, C-10.

**Work packages**

- [x] Resolve PRD D-01: begin the planned playable prototype after its visual proof, per the owner's execution request.
- [ ] Resolve D-02: confirm build 3369, DM-Rankin, selected room, fidelity tolerances, and performance target.
- [x] Confirm a separate development root: `C:\Users\brian\git-projects\ut2k4-ue5`.
- [x] Record hashes of original assets, binaries, and configuration before creating the development reference copy.
- [x] Create and hash-verify the reference copy. Use it for editor runs and baseline recordings.
- [x] Select and record the installed tool versions: UE5 5.8.3, UnrealEd/UCC build 3369, and Blender 5.2.2 LTS.
- [x] Start a basic First Person project in the separate root. [Template smoke](../Evidence/P0/ue-project-setup.json) records spawn, mouse look, jump camera response, and return to the editor. Keep the original installation outside import/output paths.
- [ ] Record a Rankin walkthrough, matching camera viewpoints, at least 10 full-map landmarks, required routes, and interactive geometry.
- [ ] Capture source and observed movement conditions: dimensions, gravity, camera, input timing, and five trials per required action.
- [ ] Capture primary fire, core impact, combo, cooldown, ammo consumption, radius/obstruction behavior, and low-ammo outcomes.
- [ ] Define the reference records, asset manifest, and phase evidence locations specified in PRS §3.

**Baseline records**

Execution evidence lives in [P0 status](../Evidence/P0/status.md). The initial Rankin Level T3D export proves source inspection only; it does not pass P0's runtime gate or P1's room-import acceptance.

The saved atrium inspection level has also passed a bounded UE5 numeric import and fresh-editor reload. [P1 import evidence](../Evidence/P1/ue-import/serialized-inspection.json) records the result. Physical calibration, collision, material/UV fidelity, and traversal checks remain open; the P1 work packages below are not yet accepted.

Continuation on 2026-10-04: the original main-menu launch passed; original configuration hashes, four template assets and two saved atrium assets remain unchanged. [Fourteen individual surface samples](../Evidence/P0/ue-landmark-samples.json) verify the provisional numeric transform. The copied executable fails before engine startup with Steam load error `0x02`. [Prepared fallback](../Evidence/P0/reference-launch-fallback.json) is unexecuted pending the owner's launch-boundary decision. D-02 tolerances and physical scale are also pending; complete the controlled runtime baseline before moving to P1 collision/material/traversal work.

The owner-authorized private snapshot was pushed as `28892c6`. Post-push decision work recommends isolated installed-executable launch verification, a 176 cm standing-cylinder correspondence (`s=2`), and fixed 2-source-unit geometry tolerances while retaining movement/performance proposals. These remain owner review items; no dependent runtime, scale or phase acceptance is recorded. [D-02 review notes](PRD-UT2004-UE5.md).

Record the original settings and actual frame rate used for each comparison.
Movement tests require matched frame-rate conditions, not an assumption that an INI limit controls every game mode.
Record source class references and inherited behavior alongside the observed trials.

**Exit evidence**

- Decisions D-01 through D-03 have the results required for P1 recorded.
- Every proposed acceptance comparison has a source, method, units, and target.
- The protected-file hashes, development boundary, and reference-copy location exist.
- The selected UE5 template runs, and the original game still launches.
- P1's room and representative content list are fixed.

**Stop or revise**

Stop dependent work if the required source map/assets cannot be inspected or the separate development boundary cannot be established.
Keep unresolved public distribution outside this local prototype. It is not a reason to pretend source content is cleared for release.

## P1 — Prove one-room recovery

**Coverage:** C-01, C-02, C-09.

**Consumes:** P0 room selection, source references, calibration method, tool versions, and original-copy map.
**Produces:** Recovered room, asset mapping, measured geometry/collision results, and a repeatable recovery procedure.

**Work packages**

- [ ] Export the selected room's brush/actor reference with UnrealEd. Preserve source transforms and texture references.
- [ ] Recover its representative static meshes and textures. Include required map-local objects rather than searching only external packages.
- [ ] Import one representative prop through the chosen interchange path. Compare pivot, axes, scale, normals, and material slots.
- [ ] Reconstruct or transfer the room geometry. Rebuild UE5 collision and preserve source layout and openings.
- [ ] Recreate texture alignment for the selected surfaces and retain the asset/source mapping.
- [ ] Apply the calibrated transform and verify the selected room's dimensions and landmarks.
- [ ] Traverse the room with the basic character. Check walls, floors, stairs, openings, and the selected representative prop.
- [ ] Repeat the recovery procedure into a clean test level to expose hidden manual steps.
- [ ] Record actual conversion time and repairs per asset and surface category.

**Exit evidence**

- Room measurements pass the locked PRS §7.1 tolerances.
- Every delivered room dependency has a manifest entry.
- The character cannot pass through tested solid surfaces or become blocked on a required room route.
- Texture alignment and prop placement agree with the reference captures.
- The repeat run produces the same evaluated layout and documents each manual repair.

**Stop or revise**

Do not assume UModel, UT4X, or a T3D importer reconstructs the map automatically.
If transfer fails, evaluate manual reconstruction only within the selected room.
Before building a converter or reconstructing the whole map manually, explain the failure and obtain a revised scope decision.

## P2 — Prove the visual payoff

**Coverage:** C-02, C-03, C-07, C-10.

**Consumes:** Accepted recovered room and matching original camera references.
**Produces:** Rankin Visual Proof, a reproducible rendering preset, and an owner decision on visual direction.

**Work packages**

- [ ] Select a bounded material list that covers the room's actual surfaces, such as metal, painted panels, masonry, and emissive elements.
- [ ] Rebuild those materials with recorded surface-response choices. Preserve the identifying patterns and colors.
- [ ] Relight the room using the initial Lumen candidate and compare shadows and reflections at matching viewpoints.
- [ ] Place a nonfunctional preview of the intended practice target for the visual review. Its combat behavior remains P3 work.
- [ ] Check route and target readability under the new lighting. Recheck collision after art changes.
- [ ] Package an early Development build and capture the room route outside the editor.
- [ ] Record warm-run frame times and cold-start preparation separately using the locked capture method.
- [ ] Produce matching original/prototype captures and record the actual art work required.
- [ ] Resolve D-04: accept the visual direction, revise it within this room, or stop.

**Exit evidence**

- The owner records acceptance of lighting, surface response, shadows/reflections, and readability.
- Room layout still passes C-02.
- The packaged room reaches the locked performance criterion with recorded native-resolution settings.
- Evidence includes the preset, camera transforms, build identity, and original/prototype images.

**Stop or revise**

If the visual preset misses the target, measure the dominant cost before changing rendering features.
A reduced preset or revised target must produce a new labeled comparison and owner decision.
If the owner selected graphics-only scope in P0, this accepted Visual Proof completes that scope. P3–P5 remain unexecuted.

## P3 — Make the room playable

**Coverage:** C-04, C-05, C-06, C-07.

**Consumes:** Accepted visual room and source-backed gameplay contracts.
**Produces:** Playable room with UT movement, Shock Rifle, stationary targets, basic HUD, and reset.

**Work packages**

- [ ] Resolve the Blueprint/C++ split for the measured movement and weapon requirements. Record authoritative class/asset locations in the PRS.
- [ ] Implement walking and strafing using the calibrated source units. Compare movement distance and acceleration behavior.
- [ ] Implement jump, double jump, dodge, dodge jump, and wall dodge under their source conditions.
- [ ] Verify the apex window and wall requirement. Reject the same unsupported action sequences as the reference game.
- [ ] Implement Shock Rifle primary fire and its observed cadence, damage, ammunition use, and obstruction behavior.
- [ ] Implement the secondary core, ordinary impact, lifetime, and collision behavior.
- [ ] Implement the shock combo, radius/momentum behavior, and measured complete ammunition accounting.
- [ ] Add stationary target fixtures, player/target state, hit feedback, and the PRS-defined HUD.
- [ ] Implement reset and out-of-world recovery. Remove existing cores and reset firing/movement state.
- [ ] Repeat gameplay trials outside the editor and run ten consecutive practice resets.
- [ ] Capture frame-time results with firing and combo effects active.

**Verification focus**

Movement: use the five-trial reference sequence for each required action.
Measure distance, apex height, and duration where each applies. Apply the locked PRS §7.2 tolerance.
Weapon: test beam hits, misses and walls, ordinary core impacts, qualifying core/beam combos, radius obstruction, cadence, and ammo depletion.
These cases are reachable in normal use and serve the selected weapon contract.
Reset: verify spawn, health, ammo, target health, movement, projectiles, and cooldown state each time.

**Exit evidence**

- Every movement action passes the locked behavioral and trajectory comparison.
- Weapon trials pass the reference contract. A source-value table alone does not pass this gate.
- Ten resets restore the specified initial state without reopening the application.
- Active gameplay reaches the locked frame-time target in the room.
- No bot AI, additional weapon, or networking work has entered the implementation.

**Stop or revise**

If built-in movement cannot match the measured behavior, isolate the demonstrated mismatch before introducing a custom component.
If gameplay reproduction requires a broader subsystem, revise the scope before committing to full-map completion.

## P4 — Complete the Rankin prototype

**Coverage:** C-01 through C-07, C-09.

**Consumes:** Proven room recovery, accepted visuals/gameplay, and measured effort from P1–P3.
**Produces:** Full playable Rankin layout with the offline practice loop.

**Work packages**

- [ ] Estimate the remaining map work from the actual room, material, prop, and gameplay costs.
- [ ] Record the owner decision to complete the map using that estimate.
- [ ] Recover and reconstruct the remaining playable spaces using the accepted pipeline.
- [ ] Reproduce the interactive geometry required by the original traversal routes, including any verified lift or mover dependency.
- [ ] Extend the accepted materials and lighting across the map. Record intentional art replacements.
- [ ] Integrate the existing movement, Shock Rifle, target fixtures, HUD, and reset behavior.
- [ ] Check at least 10 full-map landmarks and every required route against the original.
- [ ] Recheck movement in representative stairs, slopes, openings, landing areas, and wall-dodge locations.
- [ ] Verify weapon effects against actual map collision and update matched-view captures.
- [ ] Capture the three full-map performance runs and review manifest coverage.
- [ ] Compare original protected-file hashes with the P0 record.

**Exit evidence**

- Every required route is traversable and required interactive geometry functions.
- Landmark and dimension checks pass the locked PRS §7.1 criterion.
- Art changes preserve C-03 readability and the accepted visual direction.
- Gameplay and reset checks pass in the complete map.
- All three full-map captures pass the locked performance gate.
- Every delivered dependency has a source/reuse record. Original protected files match the baseline, including separately documented normal runtime configuration updates.

**Stop or revise**

If another room exposes an incompatible asset category, record its failure and bounded repair cost.
Do not turn the repair into a whole-game converter project.
Revisit the completion estimate if the remaining work exceeds the accepted map scope.

## P5 — Package, evaluate, and decide

**Coverage:** C-01, C-07, C-08, C-09, C-10.

**Consumes:** Accepted complete Rankin project and P4 evidence.
**Produces:** Rankin Combat Prototype Windows package and a documented expansion decision.

**Work packages**

- [ ] Produce the Windows Development evaluation build with its engine version and project revision/snapshot recorded.
- [ ] Provide controls, runtime prerequisites, reset behavior, selected quality preset, and known deviations with the package.
- [ ] Close the editor and launch the packaged application in three separate sessions.
- [ ] In each session, spawn, traverse, fire both modes, perform a combo, interact with a target, and reset.
- [ ] Reproduce the three full-map frame-time runs on the recorded PC.
- [ ] Compare the original protected files before launching the original game. Record any normal launch-generated configuration changes separately.
- [ ] Assemble the import, visual, movement, weapon, reset, packaging, and performance evidence.
- [ ] Update the PRS to describe the actual implementation and list remaining deviations.
- [ ] Resolve D-06: expand with a new bounded scope, correct the prototype, or stop.

**Exit evidence**

- The package completes the practice loop without an editor process.
- The recorded runtime prerequisites explain any required installed runtime.
- Gameplay, reset, asset coverage, original preservation, and packaged performance pass.
- The owner has the comparison results and a recorded next-scope decision.
- Unresolved failures remain visible. None are described as completed work.

This gate accepts a local evaluation package. Public distribution remains governed by D-05.

## Conditional expansion roadmap

These are candidate next scopes under C-10. Each requires revised requirements, evidence, and an owner decision before implementation.

| Candidate | Bounded proof | Expansion condition |
|---|---|---|
| E1 — Offline arena match | Rankin with pickups, scoring, death/respawn, and one bot opponent | The selected match loop and bot behavior have explicit acceptance criteria. |
| E2 — Weapon roster | Add one selected weapon and its interactions per increment | Movement/weapon tests prevent regressions in the accepted prototype. |
| E3 — Multiplayer proof | Rankin with two clients and one selected session topology | Validate movement and weapon replication/latency before adding modes or player counts. |
| E4 — Additional map/mode | One selected map and mode that exercise the next desired capability | Define terrain, objective, or vehicle requirements only for that selected increment. |
| E5 — Full-remake decision | Inventory remaining maps, roster, weapons, vehicles, audio, UI, and modes | Establish measured effort, release audience, content reuse conditions, and an accepted full-product scope. |

Multiplayer and additional weapons can become separate branches after P5. The sequence above is not a calendar commitment.
Onslaught requires its own terrain, vehicle, and objective feasibility work before an E4 delivery commitment.
Connecting to existing UT2004 servers remains outside this remake's current roadmap.

## Requirement coverage and evidence map

| Capability | Delivery phases | Acceptance evidence |
|---|---|---|
| C-01 Traceable content | P0, P1, P4, P5 | Asset manifest and actual delivery dependency list |
| C-02 Recognizable Rankin | P0, P1, P2, P4 | Landmarks, calibrated dimensions, full route checklist |
| C-03 Modern visuals | P2, P4 | Matched captures and owner visual review |
| C-04 UT2004 movement | P0, P3, P4 | Source-backed action contracts and controlled trajectory trials |
| C-05 Shock Rifle | P0, P3, P4 | Weapon, combo, obstruction, and ammo trials |
| C-06 Offline practice loop | P3, P4, P5 | Ten resets and packaged practice smoke test |
| C-07 Performance | P0, P2, P3, P4, P5 | Labeled frame-time captures and PRS §7.4 statistics |
| C-08 Windows execution | P5 | Three packaged launches outside the editor |
| C-09 Original preservation | P0, P1, P4, P5 | Protected-file hashes and original launch check |
| C-10 Gated expansion | All gates, especially P2 and P5 | Decision records and updated document scope |

## First execution package

Project execution has started with P0. Complete its runtime and reference gate before accepting P1 recovery work.
Its outcome must identify the selected room, engine/tool versions, reference-copy boundary, source-backed trial contracts, and locked acceptance targets.
Then prepare the detailed P1 implementation tasks using those facts.
Do not bulk-export the game, rebuild every map, or create the full gameplay stack during the reference phase.

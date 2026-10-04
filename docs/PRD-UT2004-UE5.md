# UT2004 UE5 Remake — Product Requirements Document

Status: Working draft v0.2 | Created: 2026-10-04 | Review owner: project owner

Companion documents: [PRS](PRS-UT2004-UE5.md) and [Phase Plan](PHASE-PLAN-UT2004-UE5.md).

The owner authorized initial phase execution on 2026-10-04 in `C:\Users\brian\git-projects\ut2k4-ue5`. Numeric targets remain provisional until the reference comparisons are established. The native UE5 First Person template runs, and the Flak atrium exists as a saved geometry inspection level. A playable recovered room and UT gameplay remain pending.
The working scope is one playable map, followed by evidence-gated decisions about a larger remake.

The 2026-10-04 continuation verified the original main-menu launch and fourteen individual saved-UE surface correspondences. The copied game's Steam load error blocks reference gameplay trials; an isolated installed-executable fallback, physical scale and D-02 targets await owner decisions. [Current evidence](../Evidence/P0/status.md).

## 1. Purpose & vision

Create a UE5 recreation of Unreal Tournament 2004 that improves graphics while preserving its recognizable environments and arena movement.
Use the original game, public modding references, and available gameplay scripts as the reference for fidelity.

The first release is the **Rankin Combat Prototype**: DM-Rankin, UT2004 movement, the Shock Rifle, stationary practice targets, and an offline reset loop.
An earlier **Rankin Visual Proof** demonstrates one recovered room with modern materials and lighting.
These milestones establish conversion effort, visual value, gameplay fidelity, and performance before expansion.

The long-term opportunity is a fuller UE5 remake. Its remaining maps, weapons, modes, bots, vehicles, and networking are conditional future scope.
This draft does not commit to a whole-game delivery date or public release.

## 2. Users & personas

| Actor | Need | Role |
|---|---|---|
| Project owner | Evaluate whether the graphics and gameplay results justify further work | Reviews milestones and chooses expansion scope |
| Reference player | Recognize Rankin and reproduce familiar movement and weapon actions | Compares the prototype with build 3369 |
| Developer/content author | Recover content and rebuild behavior with traceable evidence | Maintains the project, source references, and verification results |

The product is a standalone local Windows game prototype. It is neither a patch for the Steam installation nor a connected service.
The first evaluation audience is the project owner on the reference PC.

## 3. Value drivers → required capabilities

| Value driver | Required capabilities |
|---|---|
| Assess the visual benefit before committing to a remake | C-02, C-03, C-07 |
| Preserve the elements that make the result recognizable as UT2004 | C-02, C-04, C-05 |
| Make each milestone playable or independently inspectable | C-06, C-08 |
| Reduce guesswork and protect the working original | C-01, C-09 |
| Expand only after conversion and gameplay evidence exists | C-10 |

## 4. Capability catalog

The PRS implements these IDs. The Phase Plan assigns their delivery and verification gates.
Each boundary below names a failure that acceptance must detect. There are no governing ADRs yet.

| ID | Capability and actor outcome | Acceptance boundary | Observable evidence | Envelope |
|---|---|---|---|---|
| C-01 | **Traceable content.** The developer can identify the origin and conversion of every delivered asset. | A delivered asset lacks its source, conversion record, or reuse status. | Asset manifest resolves every asset dependency in the evaluated level and weapon. | Newly authored assets record authoring provenance instead of an original package. |
| C-02 | **Recognizable Rankin.** The reference player can traverse the recreated playable layout and identify its landmarks. | Required routes, geometry, prop placement, or collision differ beyond the locked fidelity target. | Landmark measurements, traversal checklist, and matched camera captures. | Visual Proof covers one selected room. Combat Prototype covers the full playable map. |
| C-03 | **Modern visuals.** The owner can inspect updated lighting, surfaces, reflections, and shadows at matching viewpoints. | The visual proof lacks a visible improvement or obscures traversal and target readability. | Original/prototype capture pairs and an explicit visual review result. | Decorative changes must preserve C-02 routes and C-04 movement tests. |
| C-04 | **UT2004 movement.** The player can walk, strafe, jump, double jump, dodge, dodge jump, and wall dodge. | An action differs from the original's permitted behavior or exceeds the locked motion tolerance. | Controlled input trials, trajectory measurements, and source parameter references. | Conditions in the original game govern whether each action is permitted. |
| C-05 | **Shock Rifle combat.** The player can use primary fire, secondary fire, and the shock combo. | Cadence, ammunition use, hit behavior, or combo triggering differs from the recorded reference contract. | Weapon trial results and cited build-3369 classes. | Trial targets have defined armor, health, and damage rules. |
| C-06 | **Offline practice loop.** The player can spawn, practice movement and combat, and reset without restarting the application. | Reset leaves ammunition, targets, projectiles, health, or player position in a previous-session state. | Repeated loop checklist and visible HUD/target state. | This release uses stationary targets and player fall/death recovery, without bot opponents. |
| C-07 | **Measured performance.** The owner can evaluate frame pacing on the recorded reference PC. | A packaged build misses the locked frame-time target or lacks reproducible capture settings. | Three route captures, frame-time statistics, settings, and hardware record. | Early room results do not satisfy the full-map acceptance gate. |
| C-08 | **Standalone Windows execution.** The owner can launch and use the prototype without opening the UE5 editor. | The packaged build cannot launch or complete the C-06 practice loop outside the editor. | Packaged-build smoke test and documented runtime prerequisites. | Existing operating-system/runtime prerequisites may be declared. |
| C-09 | **Preserved original game.** The owner retains a working build-3369 installation. | Development tools replace or modify original game assets, binaries, or configuration. | Protected-file hash comparison before the original-game launch check; normal runtime configuration changes are recorded separately. | Project documents and development outputs reside in the separate project root. |
| C-10 | **Evidence-gated expansion.** The owner chooses later scope using prototype results. | Work enters a later feature scope without a recorded gate decision and updated requirements. | Phase decision records identify evidence, selected scope, and acceptance criteria. | Research may compare future options without implementing them. |

## 5. Phased delivery

| Phase | Product result | What it proves |
|---|---|---|
| P0 — Reference and decisions | Recorded original behavior, project boundary, and locked pilot targets | Comparisons have a defined baseline |
| P1 — One-room recovery | One navigable Rankin room with recovered geometry and representative content | The content pipeline can reconstruct the selected room |
| P2 — Visual payoff | Rankin Visual Proof | The visual improvement justifies continued work at the proposed performance target |
| P3 — Playable room | Movement, Shock Rifle, targets, HUD, and reset in that room | Gameplay reproduction is achievable before completing the whole map |
| P4 — Full Rankin | Complete playable layout using the proven room and gameplay work | The approach scales across the selected map |
| P5 — Packaged evaluation | Rankin Combat Prototype and comparison results | A standalone build supports a decision about expansion |

The Phase Plan contains work packages, dependencies, verification procedures, and stop conditions.
Future options include an offline arena match, further weapons, multiplayer, more maps and modes, and vehicles.
These options are not requirements for the Rankin Combat Prototype.

## 6. Success metrics

All numeric targets below are **proposals**, not measurements or approved commitments. P0 locks them before implementation comparisons begin.
The owner may revise them using baseline evidence. A revision updates all three planning documents.

| Metric | Proposed target | Baseline and evidence |
|---|---|---|
| Delivered asset traceability | 100% of asset dependencies have manifest records | Rankin's Level T3D export exists. Check the actual UE5 delivery dependency list when a build exists. |
| Spatial fidelity | At least 10 landmarks and every required traversal route pass PRS §7.1 | Original coordinates and calibrated scale are not measured yet. |
| Movement fidelity | Each required action passes five controlled trials within 5% of reference distance, height, and duration | Source defaults exist. Observable trajectories remain unmeasured. |
| Weapon contract | Every C-05 trial passes the source-backed contract and recorded ammo accounting | Weapon scripts exist. In-game reference trials remain unrecorded. |
| Practice reset | 10 consecutive resets restore the documented starting state | No prototype exists yet. |
| Visual value | Owner accepts matched views for lighting, material response, shadows, and readability | No prototype comparison images exist yet. |
| Performance | At 1920×1080 native resolution, each warmed 90-second run has P95 frame time ≤16.67 ms | No UE5 frame-time baseline exists. A 120 FPS target is a later option. |
| Original preservation | Zero changed protected original assets, binaries, or configuration due to development | Record hashes before development access and compare before smoke launches. Keep documented runtime configuration changes separate. |
| Independent launch | Packaged build completes the practice loop in three launch sessions | The UE5 engine is not currently registered in Epic Launcher. |

## 7. Relationship to existing systems

The original Steam installation supplies the reference game and source content. Its log identifies build 3369 and D3D8 rendering.
The installed tools include UnrealEd and UCC. The reference PC has Windows 11, an i5-12400F, 32 GB RAM, and an RTX 4060 Ti with 16 GB VRAM.

The UE5 project will use separate working directories. It will coexist with the original game and will not replace its renderer or packages.
The prototype will not connect to UT2004 servers or load existing mods as executable UE5 gameplay.

Public UnrealScript and selected C++ excerpts provide behavior references. They do not provide an automatic UE5 gameplay conversion.
Original tutorials explain the old content pipeline. Their Max/Maya plugins are historical tools rather than required modern dependencies.

Research references:

- [3D Buzz UT2003/2004 training archive](https://archive.org/details/3DBuzz).
- [Epic UE2 documentation](https://docs.unrealengine.com/udk/Two/SiteMap.html).
- [Build-3369 script reference](https://github.com/Deaod/UT2004).
- [UModel](https://www.gildor.org/en/projects/umodel) and [current Blender PSK/PSA importer](https://github.com/DarklightGames/io_scene_psk_psa).
- [UT4X-Converter limitations](https://github.com/xtremexp/UT4X-Converter), which explicitly exclude UE5 support.

## 8. Risks & open questions

### Risks & mitigations

| Risk | Consequence | Bounded response |
|---|---|---|
| Map recovery loses brush geometry, UV alignment, or prop placement | Full-map reconstruction effort exceeds expectations | Prove one room in P1 before estimating the map. |
| Modern materials obscure the original art direction | The result loses recognition or gameplay readability | Review matched viewpoints in P2 and preserve routes in C-02. |
| Matching source numbers does not reproduce movement | The arena feels different despite similar settings | Compare trajectories and permitted action sequences in P3. |
| Lumen misses the proposed frame-time budget | The chosen visual preset cannot support the target | Measure P2 and P4. Revise the preset or target before expanding. |
| Public asset reuse conditions remain unresolved | A public package cannot be treated as an accepted release | Keep the first evaluation local. Resolve distribution scope before an external release. |
| Scope grows into bots, vehicles, or networking during the pilot | Conversion and fidelity evidence becomes harder to assess | Apply C-10 at P5 and define a separate acceptance scope for each expansion. |

### Decision register

This register holds deferred questions inside the requested document set. No separate backlog or ADR files are created.
The owner records each result here and mirrors its technical effect in the PRS and Phase Plan.

| ID | Decision | Current proposal | Due / disposition |
|---|---|---|---|
| D-01 | First product scope | Rankin Combat Prototype after the one-room Visual Proof | Initial execution authorized by the owner on 2026-10-04. Later phase acceptance remains evidence-based. |
| D-02 | Reference version, map, and targets | Build 3369, DM-Rankin, Flak atrium pilot, and the proposed metrics in §6 | Pending owner target/physical-scale decision in P0; runtime baseline blocked by copied-game launch error. No proposed value is accepted yet. |
| D-03 | UE5 version and gameplay implementation | UE5 5.8.3, native framework, no third-party gameplay framework | Installed version verified; native Blueprint First Person template passed a qualitative Play in Editor smoke. Select UT gameplay Blueprint/C++ boundaries before P3. |
| D-04 | Visual direction | Preserve UT2004's colors, silhouettes, and layout while rebuilding light and surface response | Review the room in P2 before full-map art work. |
| D-05 | Evaluation and distribution audience | Local owner evaluation | Resolve external distribution conditions before any external package release. |
| D-06 | Expansion scope | No later features selected | Decide after P5 using measured conversion, gameplay, and performance results. |

Post-push D-02 review package (2026-10-04, **not accepted**): select a 176 cm standing collision-cylinder height for the original 88-unit height (`2 cm/source unit`), and use fixed `<=2 source units` for sampled landmark positions and reference dimensions. Retain the five-trial/5% movement and native-1080p/P95<=16.67 ms packaged performance proposals. The current atrium percentage position allowance is 23.436587 units (46.873174 cm at scale 2); fixed 2 units is 4 cm. Owner selection updates §6, PRS §7 and the Phase Plan before dependent comparison acceptance.

The runtime-boundary recommendation is the prepared installed-executable launch with isolated ReferenceGame content and project-only runtime INIs/outputs. The owner must approve that changed boundary; effective overrides and original preservation must then be verified. Commit/push permission did not accept this launch or the scale/target package. [Decision preparation](../Evidence/P0/status.md).

There is no calendar commitment or staffing estimate. P1–P3 measurements support the first credible estimate for the remaining map work.

## 9. Out of scope

- The Rankin Combat Prototype excludes bot AI, online multiplayer, vehicles, additional weapons, and additional maps.
- It excludes a full campaign, full roster, complete game modes, and a replica of every original menu.
- It excludes UT2004 network compatibility, automatic mod loading, and a general-purpose UE2-to-UE5 converter.
- It excludes replacing the Steam installation or installing OldUnreal, ReShade, wrappers, or RTX Remix as part of this project.
- It excludes public distribution, monetization, and a whole-game shipping commitment from the first evaluation release.
- Initial phase execution is authorized. The owner separately authorized commit/push to the private `briandgibby/ut2k4-ue5` repository on 2026-10-04. Public release remains outside the execution scope.

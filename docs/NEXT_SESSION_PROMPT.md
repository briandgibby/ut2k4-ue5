# Prompt for the next UT2004 UE5 session

Copy the following into a new session:

```text
Continue the UT2004 UE5 project at C:\Users\brian\git-projects\ut2k4-ue5.

First read SESSION_CONTINUITY.md, Evidence/P0/status.md, the PRD, PRS and phase plan in docs/, and the Rankin/gameplay references in References/. Set your working directory to the project root; the original UT2004 installation must remain protected.

UE5 5.8.3 and Blender 5.2.2 are already installed. Prototype/UT2004UE5.uproject is a native Blueprint First Person project with a successful qualitative PIE smoke. The Flak atrium imported into /Game/RankinRecovery/L_FlakAtrium_Transport and passed saved-asset reload and numeric bounds checks. Reuse the existing artifacts. This level has collision disabled and grid materials; physical scale, per-corner UE UV fidelity, original appearance, and room traversal are not accepted. P0 and P1 gates remain open.

The original installed game reached its main menu and exited normally; original configuration hashes are unchanged. A final check verified all 1,607 protected originals, four template assets and both saved atrium assets. Native readback matched four noncoplanar BSP vertices and ten landmark-group mesh corners at numeric (X,-Y,Z), scale 1, with maximum error 0.0000004955. Reuse Evidence/P0/ue-landmark-samples.json; this does not establish actor pivots, physical scale or full-map landmark coverage.

Resolve the next bounded blocker: the copied ReferenceGame/System/UT2004.exe fails before engine startup with Steam Application load error (0x02). Evidence/P0/reference-game-launch.json records the attempts. An installed-executable fallback with project-only P0Runtime.ini/P0User.ini, absolute ReferenceGame paths and project log is prepared in Evidence/P0/reference-launch-fallback.json but was not executed; the owner's launch-boundary decision is still pending. Do not treat silence as approval or patch the executable. Verify effective native override/content paths and original hashes if the owner approves that route.

Complete P0 reference captures and controlled gameplay trials through the approved isolated runtime route. The gameplay reference now records source step/floor constants, Rankin's default-volume setup and TimeDilation=1.1 at normal GameSpeed=1; effective native acceleration/collision remain unmeasured. Resolve D-02 tolerances and physical scale with the owner. A proposed 176 cm standing cylinder implies 2 cm/source unit; the existing numeric transform implies 88 cm at 1 cm/unit. Neither physical correspondence was accepted. Record measured outcomes and unresolved gaps honestly. After required P0 evidence/decisions are resolved, proceed with the same atrium's P1 collision, texture/UV fidelity and basic-character traversal checks.

Follow the minimal-change policy. Preserve the original installation, four stock template assets, and existing transport evidence. The owner authorized a private Git snapshot at https://github.com/briandgibby/ut2k4-ue5; reuse the existing repository and check its status. Do not add dependencies, a converter framework, full-map reconstruction, P2 art, or P3 gameplay beyond the current gate. Inspect existing processes before launching another editor or reimporting. Continue authorized work autonomously; ask a focused question only when a material decision or scope expansion requires it.

Update the existing evidence/status, asset manifest and planning documents as appropriate, and SESSION_CONTINUITY.md before the next handoff. Report completed work, verification, and the next remaining step.
```

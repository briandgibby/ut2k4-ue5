# UT2004 UE5 prototype

Current scope: local Rankin Visual Proof followed by a Rankin Combat Prototype. P0 reference decisions/trials and P1 recovered-room acceptance remain open.

Start with [SESSION_CONTINUITY.md](SESSION_CONTINUITY.md) and [P0 status](Evidence/P0/status.md). Requirements and gates are in [docs/](docs/); source and measurement references are in [References/](References/).

The native project is `Prototype/UT2004UE5.uproject` for Unreal Engine 5.8.3. The saved Flak atrium is `/Game/RankinRecovery/L_FlakAtrium_Transport`. It currently has grid materials and collision disabled. Its transport measurements do not accept physical scale, original appearance or traversal.

This private repository contains the project, tooling, tests, planning records, measured JSON/CSV evidence, captures, retained script references, native geometry exports and checked Blender/FBX handoffs. Files preserve their recorded bytes through `.gitattributes`.

Excluded local state: the approximately 6 GB installed `ReferenceGame/` copy, credentials (`env`/`.env*`), runtime/editor logs, Unreal-generated caches/intermediates, packaged builds and Blender backup files. These remain on the reference PC. No original UT2004 executable, original game package, or private runtime INI is distributed by this snapshot. Original-asset hashes and paths remain in the preservation/provenance records. Source-derived mesh assets are retained for private evaluation; public distribution is unreviewed.

The template's generated AndroidFileServer authentication token was removed from the shared `DefaultEngine.ini` and retained under ignored local `Prototype/Saved/RepositoryPrivate/`. It is unrelated to the current Windows prototype; the remaining template configuration is preserved.

Use a separately owned UT2004 build-3369 installation to recreate the local `ReferenceGame/` boundary; verify it against the recorded source hashes before editor/export work. Do not put outputs in the original installation. Reuse the checked exports and saved UE assets for the current bounded work.

The existing standard-library checks run from the repository root:

```text
python -m unittest discover -s Tests -v
```

The five tests validate the fixed Brace01HA triangle reader. Native UE/Blender probes have separate evidence records; these tests do not accept gameplay or phase gates.

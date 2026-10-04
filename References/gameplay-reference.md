# UT2004 build 3369 gameplay reference

Recorded: 2026-10-04. Coverage: PRS C-04 and C-05; P0 source inspection.

**Status: source contract recorded; gameplay measurements not executed.** The copied `ReferenceGame/System/UT2004.exe` launch failed with Steam load error `0x02` before the engine started. The native installed game's menu smoke passed; this is not a Rankin gameplay trial. Controlled runtime trials remain unexecuted pending the approved isolation fallback. No trial results, scale conversion, runtime frame rate, or accepted tolerance are claimed here; source values remain unaccepted.

## Evidence and scope

The inspected [3369 source archive](https://unrealmassdestruction.com/downloads/ut2004scripts3369.zip) is retained at [Downloads/ut2004scripts3369.zip](Downloads/ut2004scripts3369.zip).

| Archive property | Observed value |
|---|---|
| Download size | 3,245,001 bytes |
| SHA-256 | `0CE03DF380EF252DA386FF1B609DA165F1758C63EC261B9F54D8F274C7C859E2` |
| ZIP entries | 2,604: 2,527 files and 77 directories |
| UnrealScript files | 2,512 `.uc` files |
| Other files | 15 partial native `.cpp`/`.h` files |
| Recovered subset | 36 unchanged `.uc` files under `SourceScripts/` |

The mirror supplies archive evidence, not legal clearance. Its filename identifies it as 3369, but script equivalence to the installed compiled packages has not been independently established. This is not full native engine source. The limited native fragments do not supply the movement integrator used by the comparisons below.

[SourceScripts/SHA256SUMS.csv](SourceScripts/SHA256SUMS.csv) records each extracted path, byte count, and SHA-256. Extraction preserves archive paths and bytes. [SourceScripts/README.md](SourceScripts/README.md) explains the subset. Source references below use these paths and one-based line numbers; they refer to the retained files rather than an unpinned web copy.

Lengths and velocities below use UT2004 source world units and source units per second. Times use game seconds unless the input rule explicitly accounts for time dilation. `GameInfo.SetGameSpeed` sets `Level.TimeDilation = 1.1 * GameSpeed`, so `GameSpeed=1` gives source-derived `TimeDilation=1.1` (`Engine/Classes/GameInfo.uc:585–599`). This has not been measured: record actual time dilation, game timestamps, and wall-clock time separately rather than assuming equal durations. Momentum values are engine parameters, not a claim of SI units. No source-unit-to-UE5-centimeter factor has been calibrated.

## Safe local configuration observations

Read from `F:\Program Files\steamapps\common\Unreal Tournament 2004\System\User.ini` and `UT2004.ini`. Only the listed gameplay/capture fields were retained. No keys, player names, account values, bindings containing personal text, or multiplayer logs were copied.

| File / section | Field | Observed value | Implication |
|---|---|---:|---|
| User.ini / Engine.PlayerInput | DoubleClickTime | 0.250000 | Configured dodge input interval; see frame adjustment below |
| User.ini / Engine.PlayerInput | bEnableDodging | True | Dodge input detection enabled |
| User.ini / Engine.PlayerController | DefaultFOV / DesiredFOV | 90 / 90 | Camera comparison baseline in degrees |
| User.ini / Engine.PlayerController | bLookUpStairs / bSnapToLevel | False / False | Automatic stair-view and snap settings |
| User.ini / Engine.PlayerController | bKeyboardLook | True | Capture setting to preserve |
| User.ini / Engine.PlayerController | bSmallWeapons | true | Weapon presentation setting |
| User.ini / Engine.Controller | Handedness | 1.000000 | Preserve and verify weapon-side presentation in captures |
| User.ini / Engine.Pawn | Bob / bWeaponBob | 0.006000 / True | Camera/weapon bob settings |
| User.ini / Engine.PlayerInput | MouseSensitivity | 0.750000 | Input setting; not a physical mouse-motion calibration |
| UT2004.ini / Engine.Engine | DefaultGame | XGame.XDeathmatch | Configured default game class |
| UT2004.ini / Engine.GameInfo | GameSpeed / GameDifficulty | 1.000000 / 4.000000 | Match options still need recording for actual trials |
| UT2004.ini / Engine.LevelInfo | MaxClientFrameRate | 90.000000 | Configured value only; actual offline trial frame rate unknown |
| UT2004.ini / WinDrv.WindowsClient | MinDesiredFrameRate | 35.000000 | Configured value; not an actual frame-rate measurement |
| UT2004.ini / XGame.xDeathMatch | SpawnProtectionTime | 2.000000 | Avoid fresh protected targets when measuring damage |

Configuration hashes at inspection:

- User.ini SHA-256: `2926F1B1A8C3CC8FB3A86E42D66D3ADAE737A90B545DCE21C28D093FEA22AC53`.
- UT2004.ini SHA-256: `10D3E44A89F322315A08E00FA23B2AE30AC5373ED11E31F26246E63A91E65567`.

These hashes identify the inspected inputs. The project preservation baseline is recorded separately by the P0 boundary work. Runtime options may override configuration; no active match is inferred from these files.

## Movement defaults and inheritance

Relevant chain: `XGame.xPawn → UnrealGame.UnrealPawn → Engine.Pawn → Engine.Actor → Core.Object`. Human controller chain: `XGame.xPlayer → UnrealGame.UnrealPlayer → Engine.PlayerController → Engine.Controller → Engine.Actor`. Values on `xPawn` override the larger `UnrealPawn` defaults.

| Parameter / rule | Source-derived value | Units / meaning | Retained source |
|---|---:|---|---|
| GroundSpeed | 440 | Maximum normal ground speed parameter | XGame/Classes/xPawn.uc:2459; Pawn.uc:138 |
| AirSpeed | 440 | `Pawn` describes this as maximum flying speed; do not assume it defines falling speed by itself | xPawn.uc:2460; Engine/Classes/Pawn.uc:140 |
| AccelRate | 2048 | Maximum acceleration parameter | xPawn.uc:2464; Pawn.uc:142 |
| AirControl | 0.35 | Falling control parameter; native integration not present | xPawn.uc:2447 |
| WalkingPct / CrouchedPct | 0.4 / 0.4 | Slow-walk/crouch speed fractions; distinct from ordinary 440-speed traversal | xPawn.uc:2452 |
| JumpZ | 340 | Assigned Z velocity on normal ground jump | xPawn.uc:2465; Pawn.uc:2339 |
| DodgeSpeedFactor / DodgeSpeedZ | 1.5 / 210 | Direction speed factor and Z velocity | xPawn.uc:2462 |
| MaxMultiJump / MultiJumpRemaining | 1 / 1 | One extra jump at initialization | xPawn.uc:2572 |
| MultiJumpBoost | 25 | Double-jump Z becomes `JumpZ + MultiJumpBoost = 365` | xPawn.uc:2574; xPawn.uc:2001 |
| bCanDodgeDoubleJump / bCanWallDodge | True / True | Default permission flags | xPawn.uc:2636 |
| bCanBoostDodge | False at default initialization | Declared boolean has no true default assignment in this class | xPawn.uc:24; xPawn.uc:1990 |
| Standing collision | Radius 25; half-height 44 | Cylinder dimensions: diameter 50, full height 88 | xPawn.uc:2457; Engine/Classes/Actor.uc:478 |
| Crouched collision | Radius 25; half-height 29 | Cylinder dimensions | xPawn.uc:2466 |
| BaseEyeHeight / initial EyeHeight | 38 / 38 | Offset above pawn collision center | xPawn.uc:2455; Pawn.uc:159 |
| Health / HealthMax | 100 / 100 | Inherited normal player-health defaults | Pawn.uc:2779 |
| Mass | 100 | Inherited engine parameter used by damage momentum | Actor.uc:1940; Pawn.uc:2059 |
| Collision flags | Collide actors/world; block actors; projectile target | Inherited Pawn defaults | Pawn.uc:2794 |
| PhysicsVolume.Gravity | (0, 0, -950) | Gravity field default; effective trajectory acceleration unmeasured | Engine/Classes/PhysicsVolume.uc:307 |
| GroundFriction / TerminalVelocity | 8 / 2500 | Physics volume parameters, not calibrated UE5 equivalents | PhysicsVolume.uc:312; PhysicsVolume.uc:309 |
| MAXSTEPHEIGHT / MINFLOORZ | 35 / 0.7 | Script walking constants: maximum step height / minimum floor-normal Z; runtime limits unmeasured | Engine/Classes/Actor.uc:523; Actor.uc:524 |

`DefaultPhysicsVolume` covers areas without a specified volume and inherits `PhysicsVolume` (`Engine/Classes/DefaultPhysicsVolume.uc:5`). The script supplies numeric step/floor constants, but not the native walking integrator. Effective gravity, actual clearance/step/slope limits, and braking remain unmeasured. Do not substitute a familiar UE5 default or infer jump height with an unverified gravity formula.

### Rankin map volumes and collision

The [Rankin level export](../Exports/Rankin/myLevel.t3d) contains one `DefaultPhysicsVolume`, 26 `BlockingVolume` actors, five ordinary `Volume` actors, ten `ZoneInfo` actors, and one `SkyZoneInfo`; no specialized `PhysicsVolume` actor is exported. All 1,949 exported actors reference `DM-Rankin.DefaultPhysicsVolume0`. Its actor block (lines 107–115) exports priority `-1000000` without gravity, friction, or terminal-velocity overrides. `ZoneInfo7` (lines 52384–52400) references that default volume. The Flak Room's `Volume2` (lines 60205–60215) supplies a location label, not a physics override; the retained ZIP entry `Engine/Classes/Volume.uc:8` declares `Volume extends Brush`. Jump-navigation records also retain `CalculatedGravityZ=-950` (for example, line 58066); this is source setup evidence, not a trajectory measurement.

Four blocking-volume origins lie inside the documented atrium box: `BlockingVolume7` (line 56697), `BlockingVolume10` (57971), `BlockingVolume24` (61278), and `BlockingVolume20` (61454). The retained ZIP entry `Engine/Classes/BlockingVolume.uc:22–28` defaults them to world geometry with actor blocking and no zero-extent trace blocking. Their brush definitions are exported, but runtime clearance, trace behavior, and static-mesh collision remain unverified. The visual geometry handoff alone does not establish collision fidelity.

### Normal movement, jump, and double jump

`PlayerController.PlayerWalking.PlayerMove` forms `NewAccel = aForward*X + aStrafe*Y`, removes Z, and zeroes vectors smaller than 1 (`Engine/Classes/PlayerController.uc:4387`). Its `ProcessMove` assigns pawn acceleration and processes double-jump or jump flags (`PlayerController.uc:4347`). This script does not fully specify native acceleration normalization, diagonal speed, braking, or air steering; compare those through trials.

`Pawn.DoJump` requires no crouch or crouch intent and walking, ladder, or spider physics. For normal walking physics, it assigns `Default.JumpZ` when slow walking, otherwise `JumpZ`, adds vertical base velocity for a non-world base, and enters falling (`Engine/Classes/Pawn.uc:2339`). Moving-base behavior needs a separate trial if the chosen Rankin route uses a lift.

For a fresh local human jump request, `xPawn.DoJump` takes the extra-jump branch only when all of these hold (`XGame/Classes/xPawn.uc:2026`):

1. `!bUpdating`.
2. `MultiJumpRemaining > 0` and `Physics == PHYS_Falling` via `CanDoubleJump`.
3. `Abs(Velocity.Z) < 100`, strictly below 100.
4. `IsLocallyControlled()`.

The branch sets the controller's `bDoubleJump`, calls `DoDoubleJump`, decrements remaining count, and returns true. `DoDoubleJump` applies its 365 Z impulse only when neither crouched nor wanting to crouch (`xPawn.uc:2001`). The local outer branch still decrements count even if that inner crouch guard prevents the impulse; do not describe that as a universally rejected action without a trial. Nonlocal/replayed controller flags follow a different path (`PlayerController.uc:4357`); network reproduction is outside this prototype.

The extra-jump count resets to `MaxMultiJump` on `PostNetBeginPlay` and `Landed` (`xPawn.uc:890`, `xPawn.uc:1057`). There is no extra reset inside normal `DoJump`. The action is an apex-window jump, not an unrestricted airborne jump.

### Dodge, dodge jump, and wall dodge

`PlayerInput.CheckForDoubleClickMove` exits when dodging is disabled. Directional press edges are tracked; a first direction sets a timer to `DoubleClickTime + 0.5*DeltaTime`, and a matching second direction emits that dodge request (`Engine/Classes/PlayerInput.uc:275`). The caller supplies `1.1*DeltaTime/Level.TimeDilation` (`PlayerController.uc:4394`). Thus the configured 0.25 seconds includes frame/time-dilation handling; it is not an exact wall-clock cutoff independent of frame rate.

`UnrealPlayer.PlayerWalking.ProcessMove` calls `UnrealPawn(Pawn).Dodge` for directional requests and sets `DCLICK_Active` after success (`UnrealGame/Classes/UnrealPlayer.uc:574`). The input path suppresses another directional dodge while active. After returning to walking it enters `DCLICK_Done`; the done timer must fall below -0.35 before normal detection resumes (`PlayerInput.uc:291`, `PlayerInput.uc:321`). Measure timing at landing rather than asserting a universal 0.35-second post-dodge interval.

`xPawn.Dodge` rejects crouch, crouch intent, and physics other than walking or falling (`xPawn.uc:1905`). Direction axes use pawn yaw only.

- **Walking dodge:** no wall trace is required.
- **Falling wall dodge:** `bCanWallDodge` must be true. Trace opposite the requested dodge direction. Start is `Location - CollisionHeight*(0,0,1) + wallDirection*CollisionRadius`; trace another 32 source units with extent `(1,1,1)`. It must hit world geometry or a `Mover`. A miss or another actor type rejects the dodge (`xPawn.uc:1917`). This is a concrete foot-level trace, not a generic wall-contact flag. The script applies no additional hit-normal-angle test here.

`PerformDodge` replaces horizontal velocity with `1.5*440*Dir + (oldVelocity dot Cross)*Cross`, giving 660 in the dodge direction while preserving the perpendicular component for human players (`xPawn.uc:1960`). For falling dodges it first calls `TakeFallingDamage` and adds 105 to Z when old Z is below -105. It saves Z, then assigns the new horizontal vector. The later test `bCanBoostDodge || Velocity.Z < -100` evaluates the **new** vector; if true, Z becomes saved Z + 210, otherwise it becomes 210 (`xPawn.uc:1980`). For the default yaw-only human axes and false boost flag, the assigned horizontal vector has Z zero and the latter branch sets Z to 210. Preserve this operation order rather than interpreting the test as a check of the original falling velocity.

If `bCanDodgeDoubleJump` is false the dodge clears extra-jump count; the default is true. Successful dodge sets `CurrentDir` and falling physics. A subsequent dodge jump uses the same remaining-count, crouch-impulse guard, and strict apex window as double jump. A falling dodge does not itself replenish jump count.

### Camera

`Pawn.EyePosition` returns `EyeHeight*(0,0,1) + WalkBob` (`Engine/Classes/Pawn.uc:1884`). `CalcFirstPersonView` adds that, another `Pawn.WalkBob`, view shake, and ambient shake to the supplied camera position; camera rotation adds shake to controller rotation (`PlayerController.uc:3955`). `UpdateEyeHeight` smooths vertical position and uses head-clearance traces (`Pawn.uc:1801`). A fixed camera offset of 38 alone does not reproduce the moving first-person view. Capture camera transforms, FOV, bob, and firing shake separately from pawn trajectories.

## Shock Rifle contract

Relevant chains: `ShockRifle → Weapon → Inventory → Actor`; `ShockBeamFire → InstantFire → WeaponFire → Object`; `ShockProjFire → ProjectileFire → WeaponFire`; `ShockProjectile → Projectile → Actor`; `ShockAmmo → Ammunition → Inventory`. Shock damage types derive through `UnrealGame.WeaponDamageType` to `Engine.DamageType`.

### Primary, secondary, cadence, and collision

| Field | Source-derived default | Retained source |
|---|---:|---|
| Primary damage min/max | 45 / 45 | XWeapons/Classes/ShockBeamFire.uc:67 |
| Primary TraceRange | 17000 | ShockBeamFire.uc:62 |
| Primary Momentum | 60000 | ShockBeamFire.uc:63 |
| Primary FireRate / AmmoPerFire | 0.7 sec / 1 | ShockBeamFire.uc:77; ShockBeamFire.uc:65 |
| Secondary FireRate / AmmoPerFire | 0.6 sec / 1 | XWeapons/Classes/ShockProjFire.uc:39; ShockProjFire.uc:24 |
| Secondary spawn offset | (24, 8, 0) | ShockProjFire.uc:33 |
| Core Speed / MaxSpeed | 1150 / 1150 | XWeapons/Classes/ShockProjectile.uc:200 |
| Core ordinary Damage / DamageRadius | 45 / 150 | ShockProjectile.uc:202 |
| Core ordinary MomentumTransfer | 70000 | ShockProjectile.uc:204 |
| ComboDamage / ComboRadius | 200 / 275 | ShockProjectile.uc:205 |
| ComboMomentumTransfer / ComboAmmoCost | 150000 / 3 | ShockProjectile.uc:207; ShockProjectile.uc:233 |
| Core LifeSpan | 10 sec | ShockProjectile.uc:212 |
| Core initial collision radius/half-height | 10 / 10 | ShockProjectile.uc:219 |
| Core collision after timer | 20 / 20 after 0.4 sec | ShockProjectile.uc:38; ShockProjectile.uc:66 |
| Core projectile-target flag | True | ShockProjectile.uc:221 |
| Ammo InitialAmount / MaxAmmo | 20 / 50 | XWeapons/Classes/ShockAmmo.uc:12 |

Line numbers in this table are checked against the retained files. Both fire modes use `ShockAmmo`; `Weapon.AmmoAmount` aliases matching ammo classes to mode 0. Default `Weapon.bNoAmmoInstances` is true, so the shared count uses `AmmoCharge[0]` (`Engine/Classes/Weapon.uc:210`, `Weapon.uc:2001`). InitialAmount is the ammo-class default, not a claim that every pickup/match grants precisely that amount.

On an accepted authoritative shot, `WeaponFire.ModeDoFire` consumes the shot's ammo **before** `DoFireEffect` (`Engine/Classes/WeaponFire.uc:281`). Its default `DamageAtten` is 1.0. `AllowFire` requires at least `AmmoPerFire`; a zero-ammo attempt does not run the shot effect (`WeaponFire.uc:350`).

Both modes are exclusive. `ReadyToFire` rejects a mode while an exclusive other mode is firing, when ammo is insufficient, or while its next-fire time is in the future. `StartFire` takes the maximum of the requested and other mode's next-fire times to prevent rapid alternation (`Weapon.uc:1604`). Successful default fire advances `NextFireTime += FireRate`, clamped to at least current game time (`WeaponFire.uc:319`). Nominal same-mode spacing is 0.7/0.6 seconds; a secondary-to-primary combo also waits for the secondary cooldown and the secondary button must stop holding that exclusive mode. Runtime cadence remains unmeasured. Berserk functions can change FireRate (`WeaponFire.uc:253`); the comparison fixture must exclude that modifier.

Primary starts at the instigator's eye position, plus the secondary spawn offset for a player controller, honoring weapon-centered/hand rules (`ShockBeamFire.uc:8`). `InstantFire.DoTrace` performs an actor-enabled trace. Ordinary world geometry stops the beam; non-world hits receive `45*DamageAtten` and `60000*beamDirection`. There is no distance damage falloff in this path. `InstantFire.MaxRange` can clamp trace range to fog distance between 8000 and the default range (`XWeapons/Classes/InstantFire.uc:8`). The reflective path uses `xPawn.CheckReflect` and limits the reflection loop (`InstantFire.uc:32`); shield/armor implementation is outside the fixture, but must be absent during basic damage trials.

Secondary computes its start from eye position and offset. A world trace from eye position to proposed spawn point adjusts the start when a wall intervenes, preventing through-wall spawning (`XWeapons/Classes/ProjectileFire.uc:7`). It spawns the core and scales its ordinary Damage by DamageAtten (`ProjectileFire.uc:63`). The core assigns velocity `Speed*Vector(Rotation)` and schedules the collision expansion; there is no scripted speed ramp in `PostBeginPlay` (`ShockProjectile.uc:26`). Inherited projectile defaults use `PHYS_Projectile`, cylinder collision, actor/world collision, and `bCanBeDamaged=true` (`Engine/Classes/Projectile.uc:277`). Native swept collision and lifetime expiration need trials.

### Ordinary impact, combo, and attribution

`ShockProjectile.ProcessTouch` ignores its Instigator and Owner. It handles the reflective pawn path; otherwise an actor that is not a projectile, or is a projectile target, triggers ordinary `Explode`. Another ShockProjectile can cause both cores to take their ordinary explosion path (`ShockProjectile.uc:90`). Touch dispatch uses inherited `Projectile.Touch` and its `LastTouched` handling (`Projectile.uc:170`).

An ordinary `Explode` calls radius damage only on authority, uses the ordinary values and `DamTypeShockBall`, clears collision size, and destroys the core (`ShockProjectile.uc:117`). Inherited `Projectile.HitWall` can directly damage a nonstatic, non-world actor before exploding, recording it as `HurtWall` so the radius loop excludes it (`Projectile.uc:207`). Ordinary world impact is distinct from combo detonation.

`ShockProjectile.TakeDamage` qualifies a combo only when `DamageType == ComboDamageType`, whose default is exactly `DamTypeShockBeam`; it does not check a positive damage threshold, the beam shooter's identity against the core's original instigator, or that the shooter owns the core (`ShockProjectile.uc:135`). It replaces Instigator with EventInstigator, calls `SuperExplosion`, then charges the **beam shooter's current Weapon** if present. Core ownership is therefore not a combo eligibility requirement; damage attribution changes to the beam shooter.

`SuperExplosion` uses the core location, 200 base damage, 275 radius, 150000 momentum, and `DamTypeShockCombo`, then destroys trails and the core (`ShockProjectile.uc:149`). Both ordinary and combo paths end in destruction; one damage event and removal still require runtime verification. Native `Spawn`/instigator inheritance is not supplied by the script declaration (`Engine/Classes/Actor.uc:1161`). The explicit script rule is that a pawn Owner sets Instigator in `PreBeginPlay` (`ShockProjectile.uc:18`); record actual spawned ownership in trials before relying on an inferred default owner.

### Radius falloff, obstruction, and momentum

The core inherits **Projectile.HurtRadius**, not Actor's separate implementation (`Engine/Classes/Projectile.uc:89`). For each eligible result from `VisibleCollidingActors`, it computes:

```text
dir = victim.Location - explosionLocation
dist = max(1, length(dir))
dir = dir / dist
scale = 1 - max(0, (dist - victim.CollisionRadius) / DamageRadius)
damage passed to TakeDamage = scale * baseDamage
momentum passed to TakeDamage = scale * baseMomentum * dir
```

Eligibility excludes the core itself, `HurtWall`, non-authoritative victims, and fluid surfaces. The script does **not** exclude the instigator from blast victims. `Actor.uc:1342` describes the native iterator as selecting colliding actors in radius whose location trace does not hit the world; this establishes the intended obstruction dependency, but exact native collision/radius membership and boundary behavior remain unmeasured.

The inherited `LastTouched` fallback applies to an authoritative touched actor not already cleared by the main loop. Its scale is the maximum of the usual falloff and `CollisionRadius/(CollisionRadius + CollisionHeight)` (`Projectile.uc:125`). Do not implement ordinary touch as an unconditional direct 45 plus the same splash event.

`Pawn.TakeDamage` accepts integer damage, then adjusts momentum before health reduction: walking victims with the damage type's default `bExtraMomentumZ=true` receive Z at least `0.4*length(momentum)`; self-inflicted momentum is multiplied by 0.6; momentum is divided by Mass. Surviving pawns receive `AddVelocity`; death uses its death path (`Engine/Classes/Pawn.uc:2029`, `Engine/Classes/DamageType.uc:198`). The base momentum table alone does not predict measured displacement.

Applied health damage can change through UDamage, game rules, armor/shield, immunity, and DamageScaling. The configured chain is `xDeathMatch → DeathMatch → UnrealMPGameInfo → GameInfo`; `UnrealMPGameInfo` does not override ReduceDamage. `DeathMatch.ReduceDamage` makes fresh other-instigator weapon damage zero during spawn protection; in standalone games at difficulty <=3, player self damage is halved; final damage is scaled by instigator DamageScaling (`UnrealGame/Classes/DeathMatch.uc:1506`). Local configured difficulty is 4, so the <=3 condition would not apply **if that setting is used by the actual trial**. `GameInfo.ReduceDamage` also handles neutral zones, god mode, armor, and game-rule modifiers (`Engine/Classes/GameInfo.uc:1768`). Use unarmored, unmodified, unprotected fixtures and record match options; the prototype need not add these wider systems.

### Complete ammo sequence and low ammo

For a successful self-fired core followed by a successful beam hit, with the same Shock Rifle still equipped and no ammo additions:

```text
secondary: -1
primary, before beam trace: -1
qualifying core hit: explosion happens, then ConsumeAmmo(0, 3, true)
extra charge: min(3, remaining shared rifle ammo)
```

The `true` argument caps the extra charge to available ammo (`Weapon.uc:283`; old ammo-instance fallback: `Engine/Classes/Ammunition.uc:56`). The combo does not fail when three extra rounds are unavailable, and the explosion is not conditioned on ConsumeAmmo's return value. Full source-derived nominal sequence cost is **5 rounds**, not 3. These are predicted outcomes, not captured trials:

| Ammo before secondary | Source-derived sequence outcome |
|---:|---|
| 0 | No core shot accepted |
| 1 | Core accepted, ammo becomes 0; own beam unavailable without acquiring ammo |
| 2 | Core then beam accepted; combo occurs; extra charge 0; final ammo 0 |
| 3 | Combo occurs; extra charge 1; final ammo 0 |
| 4 | Combo occurs; extra charge 2; final ammo 0 |
| >=5 | Combo occurs; extra charge 3; final ammo is starting ammo minus 5 |

Shooting an existing core omits the shooter's secondary cost: beam costs 1 plus up to 3 remaining rounds. The original core shooter does not receive the combo charge in this code. Verify attribution and depletion before asserting the complete observed cost. Weapon switching after depletion is an original-game UI consequence to record; it is not an added prototype requirement.

## Unexecuted P0 measurements and comparison method

All captured-behavior fields currently read **not measured**. PRS §7.2 proposes five successful controlled trials per required movement action and <=5% error per nonzero measured quantity. Those are proposed comparison targets; this reference does not lock D-02 or mark the P0/P3 gates passed.

| Required reference trial | Conditions to record | Measurements / outcomes still missing |
|---|---|---|
| Ground forward and strafe | Known flat start/heading, normal-speed movement, exact press/release times, actual frame rate | Acceleration, speed, distance, stop behavior, diagonal behavior where used |
| Jump | Same flat start, standing, no moving base | Apex height, horizontal distance, duration, effective gravity |
| Double jump | Jump then second press with recorded vertical velocity | Five valid trajectories; rejection/absence of impulse outside strict apex window; count and landing reset |
| Dodge | Each route-relevant direction, timed double press | Distance, apex, duration, preserved cross component, input and landing cooldown |
| Dodge jump | Valid dodge followed by apex-window jump | Distance, apex, duration; unavailable extra-jump outcome |
| Wall dodge | Selected wall and route, trace geometry, falling state, crouch state | Valid trajectory; no-wall, out-of-reach, and used-count outcomes; reachable lift behavior if required |
| Camera/collision | Standing/crouched states, FOV 90, bob settings, matched viewpoint | Actual clearance, eye smoothing/bob/shake, stairs/slopes/step/floor limits |
| Primary | Unprotected unarmored fixture, hit/miss/wall, held and tap fire | Applied health delta, cadence, obstruction, trace origin/range, momentum response |
| Core | Same fixture; direct touch, ordinary world impact, lifetime | Travel speed, collision expansion, one ordinary damage event, falloff, removal and lifetime |
| Combo | Self core plus beam; existing other core when available | One combo event/removal, shooter attribution, nominal five-round sequence, damage/momentum |
| Radius and low ammo | Fixed target centers/radii, clear and world-blocked lines; starting ammo 0–5 | Native radius membership, falloff/rounding, obstruction, self effect, depletion outcomes in table |

Record each trial's map/build, match options, active modifiers, start/end pawn transforms and velocity, input schedule, frame-rate evidence, target collision size/health, ammo at each event, camera settings, and capture/result filenames. Run on the separate reference copy. Express movement and geometry results in source units until scale calibration exists. Forbidden-action comparisons should assert the observed absence of the action rather than divide by zero displacement.

P0 still needs runtime confirmation of Rankin gravity/volume and collision behavior, controlled gameplay captures through the approved isolation fallback, source-to-UE5 scale calibration, a locked acceptance decision, and matched frame-rate conditions. No UE5 gameplay implementation is implied by this record.

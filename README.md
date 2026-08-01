# Diaper-Changing Machines - Concept Designs

10 automated, hands-free diaper-changing machine concepts modeled in Blender (via blender-mcp + Python scripting).

## Designs

| File | Name | Type | Cost | Key features |
|------|------|------|------|--------------|
| M01_gantry.blend | Gantry Changer | Stationary | Mid-high | Overhead CNC gantry, gripper/wipe/spray/dryer tool head, supply cartridge, waste chute |
| M02_changepod.blend | ChangePod | Portable | Mid | Clamshell, internal arm, jets, battery, carry handle |
| M03_robonanny.blend | RoboNanny | Stationary | High | Dual articulated robotic arms, vision bar, tool rack |
| M04_carousel.blend | Diaper Carousel | Commercial | Premium | Rotary 4-station throughput |
| M05_wallmount.blend | WallMount FoldAway | Home | Low-mid | Murphy-style fold-down, gas struts, wall-mounted assist arm |
| M06_travelsuitcase.blend | TravelSuitcase | Ultra-portable | Low | Suitcase-sized, folding legs/arm, luggage wheels, 12V |
| M07_multibay.blend | MultiBay Home Station | Home | Mid-high | 4 bays, one shared rail robot services each in sequence |
| M08_semiauto.blend | SemiAuto Budget Table | Home | Lowest | Purely mechanical: conveyor pad, foot-pedal clamp, gravity magazine |
| M09_neopod.blend | NeoPod Premium | Home flagship | Expensive | Futuristic egg pod, soft-robotics tentacle arms, UV sanitize, glow accents |
| M10_conveyor.blend | Conveyor Tunnel | Commercial | Expensive | Linear conveyor: load > remove > clean/dry > apply |

## Files

- `M01..M10_*.blend` - individual machine files (each machine in its own collection, centered at origin)
- `showroom.blend` - all 10 machines assembled as collection instances (2 rows of 5) with stage + lighting
- `renders/` - EEVEE preview renders per machine + group shots

All concepts use near-future-achievable mechanisms (gantry / robot-arm / mechanical assist), spanning budget to premium, portable to commercial throughput.

# 2026-10-11 evening (dev PC, `/lm`, one launch, one reader): the head pose turns the free camera, without spinning

Build `cab5b4db065f` from the `/pd` session (`2026-10-11-pd-head-pose-on-the-free-camera.md`). Evidence:
`dev-archive/recon/2026-10-11-the-head-pose-turns-the-free-camera/`. Video (game window only):
`E:\OBS gameplay videos\heavy-rain-vr\head-pose_2026-10-11_17-39-36.mp4`, copied to the MEGA transfer folder.

## Results (bedroom scene, free camera on)

| head pose in `heavyrain_freecam_look.txt` | picture (vs before) |
| --- | --- |
| yaw 15 | turns 329 px within 1.5 s, then holds still for 5 s (no spin) |
| removed | exactly back |
| pitch 10 | 218 px vertically |
| roll 10 | rotates |
| x 0.3 | 120 px sideways |

The game's own pose (rows, position, FOV 54.4°) logs correctly and changes as the camera flies with W.
So the outcome table's first row holds: ✅ the head-pose layer works `[measured 2026-10-11, n=1 each]`.

## The reader

Building the next step at write-up time: a 64-bit OpenXR head-pose source that feeds this layer instead of the text
file (switch `heavyrain_freecam_xr.txt`), for the simulator and then a headset.

## Automation

Self-launch ✅, menu → gameplay ✅, commands (trigger files) ✅, camera ✅ (free and posed), self-close ✅.

## NOT established

Signs and units against a real head (the headset feed will settle them); comfort; whether the film camera's cuts
interfere while the free camera is on.

# 2026-10-11 (dev PC, `/lm`, one launch, one reader): the free camera switches on, takes the view, and flies

Follows `2026-10-11-pd-free-camera-switch-built.md`. Build `d37645c9bc0c` (the `/pd` build, unchanged). Evidence:
`dev-archive/recon/2026-10-11-the-free-camera-flies/`. Video (game window only):
`E:\OBS gameplay videos\heavy-rain-vr\free-camera_2026-10-11_16-57-35.mp4`, copied to the MEGA transfer folder.

## Results

1. **The hook works.** The worker found all three functions 0.8 s after start, installed the detour, and captured
   the main view on game thread 19780 at the main menu `[verified-live 2026-10-11, n=1]`.
2. **The switch takes effect.** `heavyrain_freecam_on.txt` in the bedroom scene: free-camera byte `0 -> 1 (took
   effect)`, the object's vtable is `CAMERA_BEHAVIOR_FREE`; off with `heavyrain_freecam_off.txt`: `1 -> 0`. No crash,
   switched on twice and off twice `[verified-live 2026-10-11, n=2 each]`.
3. **It takes over the view.** With it on, two pictures 5 s apart are identical (shift 0, mean difference 1.7); with
   it off the film camera is moving again (mean difference 38) `[measured 2026-10-11, n=1 each]`.
4. **It is steered by the keyboard.** With it on, each key held 1.5 s moved the view: W forward (to the wall), S back,
   A sideways, Up arrow up and out past the trees, Left arrow turning and tilting `[verified-live 2026-10-11, n=1 each]`.
   Which key does exactly what (move vs. look) needs a slower, separate test.

## What did NOT work

- The pose logger read all zeros at `+0x224..` and NaN at `+0x360` while the camera was moving, so the pose is not
  stored there `[measured 2026-10-11]`. The reader is looking for the real offsets.

## The reader (one background helper)

Asked which inputs drive the free camera and where its pose lives; its answer arrives after this note (inbox drop
`2026-10-11-reader-free-camera-controls.md`).

## Automation (five capabilities)

Self-launch ✅; menu → gameplay ✅ (click CONTINUE, ~90 s to the bedroom); commands: the trigger files work as our own
command channel ✅; camera ✅ now free and keyboard-driven; self-close ✅ (WM_CLOSE + OK).

## Why it matters

Heavy Rain is shot with fixed film cameras. A camera we can switch on and move is the first step towards a
head-tracked view, and towards placing the player's eyes where we choose.

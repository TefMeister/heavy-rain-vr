# 2026-10-29 — `/pd` (dev PC, no launch): the game's picture goes to the headset

**The game was not launched.** Everything below was built and tested outside it.

## What changed

Until now the headset got empty frames: head tracking worked (worn 2026-10-25), but the headset stayed black by
design. The proxy now also sends the game's picture:

1. A `Present` hook (MinHook) sees each frame the game shows. Only the game's own swapchain counts; one presented on
   the headset thread, or into a window that thread made (the simulator's preview), is passed straight through.
2. Back buffer 0 crosses from the game's device to the headset thread's own device through Metro's handover
   (`xr-picture/`, copied from `staging/metro-exodus-vr/share-cpu-2026-10-15`, staging `bd0770b`): LOCK (keyed mutex
   made on the headset device), else RING (three plain shared pictures), else CPU (read back through memory). The
   game never waits.
3. The headset thread copies the newest picture into both eyes' swapchain images and sends one projection layer.
   Each view sits at the head pose the free camera drew that picture with: the update hook now records the headset
   pose it applied (`fc_pose_drawn`). So a picture that arrives late is shown where the head was, not where it is.
   Before the free camera has drawn with a headset pose, the headset's own view poses are used.

One flat picture: both eyes see the same image. Stereo is the next step.

## Settings (`heavyrain_vr.ini`, `[vr]`)

`Picture=0` goes back to head pose only. `TestPattern=1` shows red/blue instead of the game. `Lens=shape` (default)
keeps the picture's shape inside the headset's width; `headset` fills the eye (stretched); `game` / `game-h` use the
free camera's own field of view (+0x130) as vertical / horizontal. `share=lock|ring|cpu|auto`.

## How it was checked

- Self-tests: 39/39 (6 new: the drawn pose and the field of view travel from the update to the picture) and 28/28
  `[compile-verified 2026-10-29]`.
- Metro's handover tests on Heavy Rain's copy, two real devices on the GTX 1660 SUPER: LOCK, RING, CPU and the
  switch between them all pass, every pixel of ~730–750 pictures per eye checked, none torn or wrong `[measured 2026-10-29]`.
- `tests/pic_host.c`: the shipped headset thread in a stand-in game window (1280x720, a colour that changes every
  second) into the OpenXR simulator for 40 s: 2,398 of 2,401 headset frames carried the picture, LOCK worked on both
  devices, every frame was accepted, and the simulator's screenshots showed the stand-in's magenta, then green
  `[measured 2026-10-29, n=1]`.
- Build repeatable (`1cd16da51f01`), exports 51/51 match. Installed on the dev PC (old `4c38f32d65c6` kept as
  `d3d11.dll.bak-2026-10-29-pd-pre-picture`), stamped.

## What is NOT established

- Whether Heavy Rain's own device accepts LOCK (Metro's refused it and fell back to RING). The log says which way
  won and why.
- Whether the game's swapchain is the first one presented in its process (the log names the captured window).
- Which axis the field of view at +0x130 is; `Lens=game` assumes vertical `[hypothesis]`.
- Whether the picture sits at the right place when the head turns fast: the drawn pose is the one the free camera's
  last update applied, which assumes the game presents the frame it just updated `[hypothesis]`.

## Next live test (dev PC, simulator, `/lm`)

Bedroom scene, free camera on, drop `heavyrain_freecam_xr.txt`. Read `heavyrain_vr_freecam_log.txt`:
- `the game's swapchain is captured`, `eye swapchains`, `FIRST picture sent`, then `picture diag` lines with
  `with the picture` close to `headset frames` = the picture reaches the simulator. Take a simulator screenshot.
- `at the drawn pose` growing = the head pose travels with the picture.
- `share RING` or `CPU` = LOCK was refused, with the step named. No picture at all: `TestPattern=1` (red/blue proves
  the headset side alone).
- Turn the simulator head (`set_head_pose` yaw 15): the picture should turn with it and the scene stay put.

# 2026-10-12 (dev PC, `/pd`, no game launch): why the headset feed closed the game

**The game was not launched. The test program below is not the game.**

## Found

1. The simulator's own log for the failed game run (PID 13076) was created at 17:50:12.735 and is **0 bytes**: the
   runtime loaded, opened its log, and the process ended before its first line ("Runtime Starting").
2. The game ships its own `msvcp140.dll` and `vcruntime140.dll`, version **14.16** (2018). Windows has 14.51.
3. The simulator imports `_Mtx_lock` but not `_Mtx_init_in_situ` from `msvcp140.dll`: built with VS 2022 17.10 or newer,
   which needs 14.40+ `[inferred-static 2026-10-12]`, `[reported]` for Microsoft's rule.
4. A small test program running the same steps (`tests/xr_host.c`): with the Windows copy every step works, 296 frames
   and head poses in 5 s; with the game's two files beside it, it dies inside `xrCreateInstance` and the simulator
   leaves a 0-byte log `[measured 2026-10-12, n=2 each]`. Evidence: `dev-archive/recon/2026-10-12-old-cpp-runtime-closes-the-game/`.

So the load-bearing claim: **the game's old C++ runtime copy crashes the OpenXR runtime inside `xrCreateInstance`**
`[measured 2026-10-12, n=2]` outside the game. That the game run died the same way is `[inferred-static]`: same step
window, same 0-byte log.

## Built (`3673914f9785`, deployed and stamped)

- Before loading anything, the headset thread logs which `msvcp140.dll` the game uses and its version. Below 14.40 it
  **does not start** and logs `xr: STOPPED ...` with the fix, so the game stays up (`[vr] AllowOldCppRuntime=1` overrides).
- One log line before each OpenXR step (1 loader, 2 instance, 3-4 system + requirements, 5 own device, 6 session).
- Self-tests: 33/33 and 28/28; check 9 proves the version check says stop for the game's copy and go for the Windows
  one `[compile-verified 2026-10-12]`. Not run in the game.

## Not established

- Whether Heavy Rain runs with the Windows copies (the two files moved out of its folder). Microsoft's runtime is meant
  to be backward compatible `[reported]`; only a launch shows it.
- Why Windows recorded no crash event (the game may catch crashes itself) `[hypothesis]`.
- Whether the headset runtimes on the home PC (SteamVR, Meta) hit the same thing; likely, if built with a recent
  compiler `[hypothesis]`.

## Next live test (`/lm`, one launch)

Move `msvcp140.dll` and `vcruntime140.dll` out of the game folder (keep them), launch, load the bedroom scene, free
camera on, drop `heavyrain_freecam_xr.txt`. The log should show `msvcp140.dll in use: C:\Windows\SYSTEM32\...
14.51`, then steps 1-6 and `session running`.
- Game will not start without its two files: put them back; next idea is giving our thread its own runtime copy.
- `session running` and head-yaw lines: the feed works; turn the simulator's head and watch the picture.
- Dies at a later step: the log now names the step.

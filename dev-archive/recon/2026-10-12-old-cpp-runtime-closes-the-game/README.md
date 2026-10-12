# 2026-10-12 (dev PC, `/pd`, no game launch): the game's old C++ runtime copy closes it inside the OpenXR runtime

`tests/xr_host.c` (staging `heavy-rain-vr/proxy-d3d11`) runs the headset thread's OpenXR steps in a small program, not
the game, and flushes a log line before each step.

- `host-windows-runtime.txt`: run beside nothing extra, so it uses the Windows `msvcp140.dll` 14.51. Every step works:
  instance, system, requirements, own device, session, spaces, `session running`, 296 frames and 296 head poses in 5 s.
- `host-game-runtime-copy.txt`: the same program with the game's own `msvcp140.dll` + `vcruntime140.dll` (14.16, 2018)
  copied beside it. It dies inside `xrCreateInstance` (segmentation fault, exit 139), and the simulator leaves a
  0-byte log, which is exactly the signature of the 2026-10-11 game run (PID 13076: 0-byte simulator log, game gone).

Both results twice each `[measured 2026-10-12, n=2]`.

Why: the simulator imports `_Mtx_lock` from `msvcp140.dll` but not `_Mtx_init_in_situ`, which is the shape of a binary
built with VS 2022 17.10 or newer (its `std::mutex` is built in place without calling the runtime); Microsoft documents
that such binaries need `msvcp140.dll` 14.40 or newer `[reported]`. The game's folder copy is found first, so every DLL
in the game's process gets it.

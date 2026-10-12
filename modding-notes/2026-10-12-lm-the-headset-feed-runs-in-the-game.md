# 2026-10-12 (dev PC, `/lm`, two launches, one reader): the headset feed runs in the game

Evidence: `dev-archive/recon/2026-10-12-the-headset-feed-runs-in-the-game/`. Videos (game window only) in
`E:\OBS gameplay videos\heavy-rain-vr\` (`xr-feed`, `private-crt`).

## 1. With the game's old C++ runtime moved out, the feed works `[verified-live 2026-10-12, n=1]`

The game starts and plays without its own `msvcp140.dll` / `vcruntime140.dll` (14.16). The log shows Windows' copy
(14.51), steps 1-6 ok and `session running`. The OpenXR simulator's head pose moves the free camera (bedroom scene):

| simulator head pose | picture |
| --- | --- |
| yaw 15 | +328 px, then holds still |
| pitch 10 | 218 px vertically (looks up) |
| roll 10 | tilts |
| x +0.3 m | -71 px (parallax the right way) |
| back to 0 | exactly the starting picture |

The same numbers as the text-file test of 2026-10-11 (329 px, 218 px), so the feed and the pose layer agree. This
confirms the `/pd` diagnosis: the old runtime copy was what closed the game.

## 2. The reader's fix for players: the old files can stay `[verified-live 2026-10-12, n=1]`

Moving game files is fragile (Steam's "verify files" puts them back). The reader built `hooks/xr_cpp_redirect.c`
(`[vr] PrivateCppRuntime=1`, off by default): on the headset thread, before `xrCreateInstance`, it loads the modern
runtime by full path and hides the game's two old copies from load-by-name, so the OpenXR runtime binds to 14.51 while
the game keeps its own. A side-by-side manifest was tried first and does not work (the runtime DLL's own manifest
wins); archived. Outside the game: crash without it, 8/8 with it `[measured 2026-10-12, n=2]`.

Live, with the game's old files back in place: `PrivateCppRuntime: on - modern C++ runtime 14.51 loaded ...; 2 older
copies hidden`, steps 1-6 ok, `session running`, yaw 15 → +328 px, the game stays up.

## 3. The free camera's keys `[verified-live 2026-10-12, n=1 each]`

W forward, S back, A/D sideways, Q up, E down, Up/Down arrows tilt the view, Left/Right arrows turn and tilt together.
PageUp/PageDown do nothing. The mouse with no button held does nothing.

⚠️ The simulator's preview window belongs to the game process and keeps coming back over the game window; screenshots
then hold a black box. Moved off-screen before measuring.

## Installed now

`d3d11.dll` `4c38f32d65c6` (staging, the reader's private-runtime build); `heavyrain_vr.ini` with
`PrivateCppRuntime=1`; the game's own `msvcp140.dll` / `vcruntime140.dll` back in place (as shipped). Trigger files
taken out. Stamped. Previous build kept as `d3d11.dll.bak-2026-10-12-lm-pre-privatecrt`.

## Not established

Real headsets (SteamVR, Meta runtimes on the home PC); the picture is still one flat view (no stereo yet); signs and
units against a real head; comfort.

## Automation

Self-launch ✅ x2, menu → gameplay ✅ (hover CONTINUE, verify, click), commands ✅ (trigger files + simulator pose),
camera ✅ (free camera, keys mapped), self-close ✅ x2 (WM_CLOSE + OK on the exit box).

# 2026-10-11 — `/pd` (dev PC): the free-camera switch is built into our d3d11 proxy

**The game was not launched, and nothing here has been run in it.**

## What was built

`staging/heavy-rain-vr/proxy-d3d11/hooks/freecam.c` (+ `freecam_settings.h`), compiled into the same
`d3d11.dll` as the generated pass-through proxy. It follows the reader's recipe
(`dev-archive/recon/2026-10-11-config-txt-does-nothing/reader-free-camera-recipe.md`):

1. A DLL constructor starts a worker thread (the constructor itself only does that, because it runs under the loader lock).
2. The worker waits up to 120 s for the Steam wrapper to decrypt the code, checking the three signatures at their
   expected addresses every 250 ms; if they never appear there, it scans `.text` once and refuses a non-unique hit.
3. It detours `GetCameraDirector` (RVA `0x2673F0`) with a 5-byte jump, written as one aligned 8-byte swap (the
   function is 16-aligned), through a trampoline that replays the stolen `mov [rsp+8], rbx`.
4. Numpad 1 (game window in front) or a trigger file only sets a request. The detour, on whichever thread asks for
   the main view (index 1), consumes the request and calls `MakeFreeCam(viewport, 1)` or `DisableFreeCam(viewport, 1)`.
5. It logs the director's `+0xA1` byte before and after each call, so the log says "took effect" or "NO CHANGE"
   without anyone judging the picture. While on, it logs the free-camera object's float blocks when they change.

## What is established

- All five signatures are unique in the unwrapped copy, at the recipe's addresses; none appear in the shipped
  (encrypted) exe, which is why the worker waits for decryption `[inferred-static 2026-10-11]`.
- `MakeFreeCam` resolves the director itself (through `[viewport+0x58]`, `0x4EE3F0`, `0x4EC410`) and does not call
  `GetCameraDirector`, so calling it from inside the detour cannot recurse `[inferred-static 2026-10-11]`.
- The free-camera handle is read the game's own way: `+0x30 & 0x202000` and a non-null `+0x50`; the logger never
  takes the slow path (`0xAC2F30`), which may load objects `[inferred-static 2026-10-11]`.
- Builds with zero warnings; exports match the system dll (51/51); self-test 21/21 against a fake function whose first
  24 bytes are the real signature; loads into a non-game host and steps aside `[compile-verified 2026-10-11]`.
- Deployed to the dev PC's game folder and stamped (`d37645c9bc0c`, 95,744 bytes).

## What is NOT established

- That `GetCameraDirector` is called with index 1 on a thread where `MakeFreeCam` is safe `[hypothesis]`.
- That the free camera, once on, actually takes the view; and which keys move it on PC `[hypothesis]`.
- That `+0x224..+0x278` / `+0x360..+0x36C` are the pose `[hypothesis]`.

## The next run (`[FLAT]`, one launch)

Launch with the deployed dll, `CONTINUE` into the bedroom scene, press numpad 1 (or drop `heavyrain_freecam_on.txt`).
Read `heavyrain_vr_freecam_log.txt`:

| log says | means |
| --- | --- |
| no `main view captured` line | the detour never sees index 1: hook a different caller (the debug menu's `SetFreeCam` route) |
| `0 -> 1 (took effect)`, picture unchanged | the byte flips but the view is not taken over: try the debug menu route (`SetFreeCam` + `PlaceFreeCam`) |
| `0 -> 1 (took effect)`, picture leaves the film camera | ✅ the switch works; next, find what moves it (pose floats while pressing keys / moving the mouse) |
| `NO CHANGE` | the call returned without setting the byte: read the function again |
| crash on switching | wrong thread: move the call to a later point on the game thread |

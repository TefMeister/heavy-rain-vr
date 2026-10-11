# Engine Dossier — Heavy Rain (Quantic Dream's in-house engine)

> One consolidated, living reference for this game's engine, filled in as the
> `PLAYBOOK.md` phases are worked. Chronological blow-by-blow belongs in the
> `dev-archive/` and `modding-notes/` folders; this file is the *distilled current
> truth*. Update it whenever a fact changes; correct false leads in place.

**Status:** M0, first static look (2026-09-15); the game has not been launched yet. · **VR-readiness verdict:** TBD.

## 1. Identity
- Game / build / version: Heavy Rain, Steam build (app 960910), exe `HeavyRain.exe` (linked 2020-05-12).
- Platform & store; unofficial port? (extra fragility/legal notes): Steam (PC). Official release, not a fan port.
- Legitimacy: owned copy confirmed.

## 2. Engine lineage
- Family / base engine and how it was modified: Quantic Dream's own engine `[reported]`. Havok and Bink 2 are in use; a comment in the exe credits CryEngine 3's temporal anti-aliasing method, which is a borrowed technique, not a sign of CryEngine `[inferred-static 2026-09-15]`.
- Middleware (animation, audio, physics, megatexture, CUDA, etc.):
- Distinctive file formats / build tags / symbol naming: Data under `Resources\` and `Videos\`, not yet looked at.

## 3. Binary & memory
- 32/64-bit, size, module base, ASLR behaviour (stable base? relocations?): **64-bit** (PE32+), `HeavyRain.exe` 25.0 MB, image base `0x140000000`, ASLR on. ⚠️ Carries a `.bind` section and its `.text` has entropy 8.0 — the shape of the **Steam DRM wrapper**, which encrypts the code on disk `[inferred-static 2026-09-15]`.
- Renderer API (D3D11/12, DXGI, GL, Vulkan) with evidence: Direct3D 11: `d3d11.dll` and `d3dcompiler_43.dll` in the import table `[inferred-static 2026-09-15]`.
- Developer console / cvar system present? how opened?: not yet investigated.

## 4. DRM / anti-debug & injection foothold
- DRM (CEG/Denuvo/GOG/none); launch-time-debugger behaviour: Steam DRM wrapper (see above). No Denuvo string `[inferred-static 2026-09-15]`. Not tested live.
- Attach workflow that works: not yet tested.
- Injection vector that works (proxy DLL name / injector / framework): not yet tested.

**🎮 2026-09-17 (home PC `RTX`, `/lm`) — FIRST LIVE LOOK.**
- **Runs:** Launches from Steam and reaches the main menu in ~30 s `[verified-live 2026-09-17, n=2]`.
- **With our file added:** A 64-bit `d3d11.dll` proxy next to `HeavyRain.exe` loads, resolves 51/51 exports, logs `D3D11CreateDevice`, and the game reaches the main menu `[verified-live 2026-09-17, n=1]`. The proxy comes from the shared generator `staging/_shared/proxy-gen/` (every export of the real system dll re-exported with the same ordinals; first call of each export logged). 
- **Windowed (for measuring; 1280×720 keeps aspect-keyed numbers the same on both PCs):** In-game Options → Graphics: Display Mode = Windowed, Resolution = 1280×720, **F** = Apply, then confirm the 15-second keep-settings prompt (the user confirmed it by hand). Stored in `<game>\user_setting.ini` `[GRAPHIC_SECTION]` `Resolution=1280 x 720`, `ScreenMode=2` (**2 = Windowed**) `[verified-live 2026-09-17, n=2]`.
- **Driving it:** Menus are mouse-driven: click at screen coordinates; Esc = back. The resolution list wraps (right from the largest goes to 640×480). `WM_CLOSE` opens a Win32 `ARE YOU SURE YOU WISH TO EXIT GAME?` box; its OK button accepts `BM_CLICK`.
- **Dead ends:** Enter from the keyboard did not confirm the keep-settings prompt; it reverted after its timer `[verified-live 2026-09-17, n=1]`.

**🖥️ 2026-10-11 (dev PC, `/lm`, five launches) — FIRST RUN HERE; WINDOWED BY THE MENU, NOT THE FILE.**
- **Runs as shipped** to the main menu (borderless 1920x1080 by default) `[verified-live 2026-10-11, n=1]`.
- ⚠️ **`user_setting.ini` is written, not obeyed, at launch:** with `ScreenMode=2` + `Resolution=1280 x 720` in the file
  (once alone, once inside the game's full list) the game still started borderless at 1920x1080, and its menu showed
  BORDERLESS; with `ScreenMode=1` the same `[verified-live 2026-10-11, n=3 launches]`. A file with only the two keys was
  overwritten with the full default list. So the 2026-09-17 "2 = Windowed, edit the file" note does not hold here.
- **The menu route works unattended:** Options (0.363, 0.486) → Graphics (0.385, 0.615); Display Mode right arrow
  (0.401, 0.385) once → WINDOWED; Resolution left arrow (0.241, 0.325) 13 times from 1920x1080 → 1280x720 (read each
  value); **F** = Apply; then **click YES** (0.195, 0.703 of the now 1280x720 window) inside the 15 s timer (a click
  works where Enter did not). The window then measured client 1280x720, desktop untouched, and stayed so on the next
  launch `[verified-live 2026-10-11, n=2 launches]`. The file afterwards reads `ScreenMode=2`, so where the game really
  keeps it is not established (the profile/save, `[hypothesis]`).
- **Music:** Options → Sound → MUSIC down arrow (0.456, 0.596), about 3 per click, to 0, then Enter (VALIDATE); voices
  and effects stay 100. `MusicVolume=0` in `user_setting.ini` was ignored, so this too lives in the profile `[verified-live 2026-10-11, n=1]`.
- The dev PC's game is at `D:\Program Files (x86)\Steam\steamapps\common\HEAVY RAIN`; `CONTINUE` loads the opening
  bedroom scene (Steam Cloud save).

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**: **most likely per-draw MVP** (2026-09-28, `/pd`): the
  exe's 227 DXBC shaders (readable in `.rdata` despite the Steam DRM wrapper) use one buffer `ConstentValue` (sic)
  with D3D9-style `register0…` variables; the biggest group (74) names +0 `modelViewProj` `[inferred-static
  2026-09-28, n=227]`. Material shaders are probably in the compressed `BigFile_WIN.*` and unread. Engine: Quantic
  Dream **ICE**; built-in **free camera** in `CameraSystem\CameraDirector.cpp` ("Integrated FreeCamera", a full
  `FreeCam_*` action set) and a `CAMERA MODIFIER DEBUG MENU`. Detail:
  `dev-archive/recon/2026-09-28-debug-menu-free-camera-and-shaders/`.
- **Free camera, how it is switched (2026-10-11, reader, unwrapped copy):** only by the Lua methods `ViewportMakeFreeCam` /
  `ViewportDisableFreeCam` (bound near `0x140267FFF` / `0x140268077`); every CameraDirector builds the "Integrated
  FreeCamera" object (`0x1403D2680`); the debug-menu " Free camera :" pages only display byte `+0xA1` of a camera object;
  `FreeCam_*` actions registered in `0x1403E3160`. No key, setting or switch turns it on `[inferred-static 2026-10-11]`.
  Route: call the native function from our own proxy.
  **Recipe (reader, 2026-10-11, RVAs from `0x140000000`, x64 calls) `[inferred-static 2026-10-11]`, untried:**
  `MakeFreeCam(viewport, 1)` RVA `0x263B10` (unique signature `40 57 48 83 EC 30 48 C7 44 24 20 FE FF FF FF 48 89 5C 24
  48 8B DA 48 8B 49 58`); `DisableFreeCam(viewport, 1)` `0x263C50`; or the debug menu's way, `SetFreeCam(director, bool)`
  `0x291490` then `PlaceFreeCam(director, director+0x230)` `0x291520`. No global pointer: detour
  `GetCameraDirector(viewport, idx)` `0x2673F0` (signature `48 89 5C 24 08 57 48 83 EC 20 48 8B D9 8B FA 48 8B 49 58 48 85
  C9 74 34`, 37 callers, game-logic thread), keep the viewport when `idx == 1`, and make the call there on a flag set
  from Present (never from Present itself `[hypothesis]`). Director: vtable `0xCEDCE8`, `+0xA1` free-cam byte, `+0x90`
  activation slot, `+0x1F8` handle to the `CAMERA_BEHAVIOR_FREE` object (vtable `0xCF1A90`), `+0x230` current shot.
  Free-cam update `0x3E24D0` reads the `FreeCam_*` actions (PC key bindings unknown); pose probably at `+0x224..+0x278`
  `[hypothesis]`. Full addresses: `dev-archive/recon/2026-10-11-config-txt-does-nothing/reader-free-camera-recipe.md`.
  **Built (2026-10-11, `/pd`):** the switch is in our d3d11 proxy (`staging/heavy-rain-vr/proxy-d3d11/hooks/freecam.c`):
  numpad 1 or a trigger file → request → `MakeFreeCam`/`DisableFreeCam` inside the `GetCameraDirector` detour, logging
  the `+0xA1` byte before/after and the free-camera floats. All five signatures unique in the unwrapped copy;
  `MakeFreeCam` does not call `GetCameraDirector`, so no recursion `[inferred-static 2026-10-11]`. Self-test 21/21
  `[compile-verified 2026-10-11]`; not run in the game. Note: `modding-notes/2026-10-11-pd-free-camera-switch-built.md`. The Steam stub was unwrapped with Steamless v3.1.0.5 (atom0s) on a
  copy kept on E: (`SteamStub 3.1 x64`) `[measured 2026-10-11]`; addresses are for image base `0x140000000`.
- Exact constant-buffer slot, parameter name(s), byte offset(s), layout,
  handedness, row/column convention:
- Where projection `P` / FOV comes from:
- The per-eye override maths (`K_eye = …`):

## 7. Constant-buffer fill mechanism
- Map/DISCARD ring / UpdateSubresource / D3D11.1 offset / **persistent map +
  memcpy** (trap):
- Can source contents be read cheaply (captured CPU pointer) or need staging
  read-back?:
- The chosen override patch point and why:

## 8. Pass inventory (by render target)
- Main scene (res/formats):
- Shadow passes (depth-only sizes):
- Post / AA chain (SMAA/TAA/motion vectors; downscale sizes):
- UI / HUD (how it's kept separate):

## 9. cvar / console cheat sheet
| command / cvar | effect | use |
|---|---|---|
| `DebugMenu`, `Cheat`, `ScriptMenu`, `ViewerMode`, `Fullscreen`, `ResolutionX/Y`, `WindowOnTop`, `EnableLuaPrint`, `LUAFile` … | a developer settings table in the exe; the exe also names `config.txt` and `user_setting.ini` `[inferred-static 2026-09-28]` | where it is read from is unknown `[hypothesis]`: the `[FLAT]` row tests `config.txt` beside the exe |

## 10. Autonomous harness recipe (this game)
- Launch to a known scene (commands used):
- In-process input / camera drive method that worked:
- Frame-capture method; where images land:

## 11. Dead ends & false leads (save future time)
- **`config.txt` beside the exe does nothing** (`DebugMenu=1`, `Cheat=1`, `Fullscreen=0`, `ResolutionX/Y`): main menu
  and gameplay unchanged, no overlay `[verified-live 2026-10-11, n=1]`. Static, on a Steamless-unwrapped copy: the boot
  code builds the path `<exe>\config.txt` and never opens it; the developer table's file loader has no callers; nothing
  reads `DebugMenu` or `Cheat`; the command line takes only `-nofocus`, `-debugdevice`, `-enablemarker`, `-renderdoc`
  `[inferred-static 2026-10-11]`. Detail: `dev-archive/recon/2026-10-11-config-txt-does-nothing/` and the reader note in §6.
- `user_setting.ini` edits for window mode and music: ignored at launch (§4).

## 12. Open risks toward the North Star
- ⚠️ The Steam DRM wrapper encrypts the code on disk, so static reading of the code needs it unwrapped first (Steamless, a public tool, is the usual route) `[hypothesis]`.
- ⚠️ **Heavy Rain is played almost entirely through fixed, film-style cameras.** A head-tracked first-person view is not how this game is built, so the realistic first goal is probably a large 3D screen in the headset rather than being inside the scene `[hypothesis]`.

## 2026-10-11 (`/lm`, dev PC): the free camera switches on, takes the view, and flies

- `d37645c9bc0c` (the `/pd` build): detour on `GetCameraDirector` found and installed 0.8 s after start; main view
  captured on the game thread at the main menu; `MakeFreeCam` / `DisableFreeCam` via trigger files flip the director's
  `+0xA1` byte `0 -> 1` / `1 -> 0`, object vtable `CAMERA_BEHAVIOR_FREE`, no crash `[verified-live 2026-10-11, n=2 each]`.
- With it on, the picture is still (5 s apart: shift 0, mean difference 1.7; with it off: 38) `[measured 2026-10-11]`.
- **Keyboard steers it:** W forward, S back, A sideways, Up arrow up, Left arrow turns and tilts
  `[verified-live 2026-10-11, n=1 each]`. Exact key-to-axis mapping not yet measured.
- The pose is NOT at `+0x224..+0x278` (all zeros while moving) nor `+0x360` (NaN) `[measured 2026-10-11]`.
- Note and evidence: `modding-notes/2026-10-11-lm-the-free-camera-flies.md`, `dev-archive/recon/2026-10-11-the-free-camera-flies/`.
- **Reader, the same day, unwrapped copy `[inferred-static 2026-10-11]`** (supersedes the recipe's "Moving it" part,
  which had the two functions swapped): vt+0x298 = `0x3E24D0` is the ACTION handler `(this, actionId, float value)`;
  vt+0x2D0 = `0x3E1F00` is the per-frame update `(this, float dt)`, returning `this+0xE0`. Actions (registered in
  `0x3E3160`): 0x1F-0x24 strafe forward/back/up/down/left/right (+0x1D4..+0x1E8), 0x25-0x28 turn up/down/left/right
  (+0x1EC..+0x1F8), 0x29/0x2A roll, 0x2B/0x2C focal, 0x2D/0x2E speed, 0x30 reset, 0xFF look at player, 0x31-0x3C depth
  of field, 0x3D/0x3E sprint. Default bindings go to pad devices 2/3 only (PS3 codes; left stick moves, right stick
  turns, d-pad up/down and roll, LB/LT zoom, RB/RT speed); no keyboard code is bound, yet the keyboard steered it live,
  so the PC layer maps keys onto the pad actions `[hypothesis]`. **Pose:** `this+0xE0` is a 0xB0-byte camera block;
  world matrix at **+0xF0..+0x12F** (rows right, up, back, then position xyz at **+0x120**), FOV in radians at
  **+0x130**. Route for head tracking: write that matrix right after vt+0x2D0 returns, on the game thread `[hypothesis]`.

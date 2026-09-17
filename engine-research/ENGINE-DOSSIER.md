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

## 5. Threading & frame structure
- Immediate context only, or deferred contexts + command lists?:
- Which thread(s) do what; render-thread name(s):
- One-frame walkthrough (record → replay → present):

## 6. Camera & projection delivery (the crucial section)
- How the world transform reaches the GPU (shared VP buffer / per-draw MVP /
  other), with **shader-reflection / disassembly evidence**:
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
| | | |

## 10. Autonomous harness recipe (this game)
- Launch to a known scene (commands used):
- In-process input / camera drive method that worked:
- Frame-capture method; where images land:

## 11. Dead ends & false leads (save future time)
- none yet.

## 12. Open risks toward the North Star
- ⚠️ The Steam DRM wrapper encrypts the code on disk, so static reading of the code needs it unwrapped first (Steamless, a public tool, is the usual route) `[hypothesis]`.
- ⚠️ **Heavy Rain is played almost entirely through fixed, film-style cameras.** A head-tracked first-person view is not how this game is built, so the realistic first goal is probably a large 3D screen in the headset rather than being inside the scene `[hypothesis]`.

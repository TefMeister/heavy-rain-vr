# 2026-09-17 — first live look: Heavy Rain

Home PC `RTX`, `/lm` session. The user asked for a first look at six games: does each run, and does it still run with our own file added.

## Does it run?

Launches from Steam and reaches the main menu in ~30 s `[verified-live 2026-09-17, n=2]`.

## With our file added

A 64-bit `d3d11.dll` proxy next to `HeavyRain.exe` loads, resolves 51/51 exports, logs `D3D11CreateDevice`, and the game reaches the main menu `[verified-live 2026-09-17, n=1]`. The proxy comes from the shared generator `staging/_shared/proxy-gen/` (every export of the real system dll re-exported with the same ordinals; first call of each export logged). 

## Windowed mode

In-game Options → Graphics: Display Mode = Windowed, Resolution = 1280×720, **F** = Apply, then confirm the 15-second keep-settings prompt (the user confirmed it by hand). Stored in `<game>\user_setting.ini` `[GRAPHIC_SECTION]` `Resolution=1280 x 720`, `ScreenMode=2` (**2 = Windowed**) `[verified-live 2026-09-17, n=2]`.

## How it was driven

Menus are mouse-driven: click at screen coordinates; Esc = back. The resolution list wraps (right from the largest goes to 640×480). `WM_CLOSE` opens a Win32 `ARE YOU SURE YOU WISH TO EXIT GAME?` box; its OK button accepts `BM_CLICK`.

## Dead ends

Enter from the keyboard did not confirm the keep-settings prompt; it reverted after its timer `[verified-live 2026-09-17, n=1]`.

## Not established

- Nothing past the menus: no gameplay was loaded, no camera data read.
- Every result is from one machine (`RTX`, 21:9 desktop) on one day.

## Next

- [PD] unwrap the Steam DRM layer on a copy (not the install), then read the code: console/debug strings, how the camera reaches the GPU, and fill in dossier §2–4
- [PD] add a swap-chain `Present` + constant-buffer logger to the shared proxy generator (same job as Burnout/DXMD)
- [FLAT] run that logger windowed through the first playable scene and read which cbuffer carries the camera

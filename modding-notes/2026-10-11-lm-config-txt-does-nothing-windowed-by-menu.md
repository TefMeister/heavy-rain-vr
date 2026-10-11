# 2026-10-11 (dev PC, `/lm`, five launches, one reader): `config.txt` does nothing; windowed through the menu

First Heavy Rain run on the dev PC. Evidence: `dev-archive/recon/2026-10-11-config-txt-does-nothing/`. Video (game
window only): `E:\OBS gameplay videos\heavy-rain-vr\debug-settings-test_2026-10-11_15-59-01.mp4`, copied to the MEGA
transfer folder.

## Results

1. **Runs as shipped** to the main menu, borderless 1920x1080 `[verified-live 2026-10-11, n=1]`.
2. **The settings file is not what the game obeys at launch.** `ScreenMode=2` or `1` with `Resolution=1280 x 720` in
   `user_setting.ini` still started borderless 1920x1080; a file with only those keys was replaced with the full default
   list `[verified-live 2026-10-11, n=3]`. This corrects the 2026-09-17 note ("2 = Windowed").
3. **Windowed 1280x720 through the menu, unattended:** Display Mode → WINDOWED, Resolution → 1280x720 (read each value),
   F, then a **mouse click on YES** inside the 15 s timer. Measured client 1280x720, desktop untouched, kept on the next
   launch `[verified-live 2026-10-11, n=2]`. Click positions in dossier §4.
4. **Music off** through Options → Sound (MUSIC to 0, VALIDATE); the file key `MusicVolume` was ignored.
5. **`config.txt` with `DebugMenu=1`, `Cheat=1`, `Fullscreen=0`, `ResolutionX/Y`:** main menu unchanged, gameplay
   (the bedroom opening) with no overlay `[verified-live 2026-10-11, n=1]`. Taken back out; kept in the evidence folder.

## The reader (one background helper)

Unwrapped a copy of the exe with Steamless (official atom0s release, downloaded to `E:\claude video game stuff\tools\
steamless\`; the copy stays on E:, never committed) and read the code: the boot code builds the `config.txt` path and
never opens it; nothing reads `DebugMenu` or `Cheat`; the command line takes only four unrelated switches; the free
camera is switched only by the Lua methods `ViewportMakeFreeCam` / `ViewportDisableFreeCam` `[inferred-static
2026-10-11]`. Second job, running at write-up time: the recipe for our proxy to call that function.

## Automation (five capabilities)

Self-launch ✅ (`steam://rungameid/960910`, ~45 s); menu → gameplay ✅ (click CONTINUE, ~35 s load into a scene);
commands N/A (no console reachable); character + camera not tried; self-close ✅ (WM_CLOSE, then OK on the Win32 box,
also from gameplay) five times.

## NOT established

Where the game really stores the window mode and music (profile/save is the guess); anything about the free camera live.

# 2026-09-28 — /pd: a developer settings table with `DebugMenu`, a whole free camera, and 227 readable shaders

Dev PC, `/pd`, no game launched, nothing run. Game at `E:\SteamLibrary\steamapps\common\HEAVY RAIN`.

The Steam DRM wrapper encrypts only the code; the exe's `.rdata` (9.8 MB) is readable as it sits on disk. Everything
below comes from there `[inferred-static 2026-09-28]`.

## 1. A developer settings table

One contiguous list of setting names in `HeavyRain.exe`:

`DatabaseConnect, Fullscreen, ScriptMenu, NoSound, DatabaseName, UserDBLogin, Bigfile, LUAFile, ResolutionX,
ResolutionY, DatabankFile, RecordObjectLoadings, EnableDataContainer, EnableVibration, Cheat, NoMessageBox,
LoadingMsg, RetrieveLog, DataVersion, DebugMenu, QdtErrorOnForceLoad, PS3Emulation, ScriptOutput, Shadows,
ForcePackedMode, WindowOnTop, ViewerMode, USMode, RemoteFileServer, RemoteFileDir, EnableRemoteFile, EnableNetwork,
RemoteMemoryViewer, ServiceSignature, TVDisplayMode, GameManager, EnableCache, ClearCache, FSAAMode, AddBigfile,
EnableLuaPrint, EnableRemoteService`

Filenames the exe names: `config.txt`, `user_setting.ini`, `gpudetect.ini`. None of the first two is in the install
folder. **Where the table is read from (a `config.txt` beside the exe, `user_setting.ini`, or the command line) is not
known** `[hypothesis]`. It is the cheapest test on this project: one text file, one launch.

## 2. A free camera and camera debug menus, built in

- `Integrated FreeCamera`, in `...\ICE\Engine\ScriptInterface\Sources\CameraSystem\CameraDirector.cpp` (the engine is
  Quantic Dream's **ICE**).
- A full set of free-camera actions: `FreeCam_StrafeForward/Backward/Left/Right/Up/Down`, `FreeCam_TurnLeft/Right/Up/Down`,
  `FreeCam_RollLeft/Right`, `FreeCam_SpeedIncrease/Decrease`, `FreeCam_Sprint`, `FreeCam_LookAtPlayer`, `FreeCam_Reset`,
  focal and depth-of-field controls, plus a `Gameplay_FreeCam_*` set.
- `CAMERA MODIFIER DEBUG MENU` (with "There is no Camera Modifier Head Activated." and
  `CAMERAMODIFIERS.GetCameraModifierHead`), a debug-menu line ` Free camera : true/false`, `MPAR ELEMENT MASH DEBUG MENU`.

**Why it matters:** Heavy Rain's cameras are fixed, directed shots. A free camera the engine already supports is the
natural base for a head-driven view, and `CameraDirector` is where the directed shots are chosen.

## 3. The shaders in the exe

227 DXBC shaders with reflection intact (`dxbc-reflect.py`). Nearly all use one constant buffer named
**`ConstentValue`** (sic) or `ConstantValue`, whose variables are called `register0`, `register1`, … — a D3D9/PS3-style
register file carried into D3D11. The largest group (74 shaders, 3904 bytes) names its first variable
**`modelViewProj`**, a per-object premultiplied matrix at +0 `[inferred-static 2026-09-28, n=227]`.

**What it means:** the camera most likely reaches the GPU **pre-multiplied into each object's matrix**, as Far Cry 2's
did, so a per-eye edit needs the view and projection from elsewhere (the CPU camera, or a matrix the engine also
uploads) `[hypothesis]`. ⚠️ These are only the shaders compiled into the exe; the game's material shaders are
probably in the compressed `BigFile_WIN.*` archives (no DXBC visible in `BigFile_WIN.dat`).

## NOT established

- How to switch on `DebugMenu` / `Cheat` (file or command line).
- Whether the free camera survives in the PC build or is compiled out behind the menu.
- Whether `modelViewProj` is what the world pass uses.

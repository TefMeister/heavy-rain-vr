# First static look (2026-09-15)

Read from the installed Steam copy on the home PC (`C:\Steam\steamapps\common\HEAVY RAIN`), without launching the game.
Every claim below is `[inferred-static 2026-09-15]` unless tagged otherwise: it comes from reading file
headers and strings, not from running anything.

- **Install:** 35 GB.
- **Identity:** Heavy Rain, Steam build (app 960910), exe `HeavyRain.exe` (linked 2020-05-12).
- **Engine:** Quantic Dream's own engine `[reported]`. Havok and Bink 2 are in use; a comment in the exe credits CryEngine 3's temporal anti-aliasing method, which is a borrowed technique, not a sign of CryEngine `[inferred-static 2026-09-15]`.
- **Binary:** **64-bit** (PE32+), `HeavyRain.exe` 25.0 MB, image base `0x140000000`, ASLR on. ⚠️ Carries a `.bind` section and its `.text` has entropy 8.0 — the shape of the **Steam DRM wrapper**, which encrypts the code on disk `[inferred-static 2026-09-15]`.
- **Renderer:** Direct3D 11: `d3d11.dll` and `d3dcompiler_43.dll` in the import table `[inferred-static 2026-09-15]`.
- **Protection:** Steam DRM wrapper (see above). No Denuvo string `[inferred-static 2026-09-15]`. Not tested live.
- **Other:** Data under `Resources\` and `Videos\`, not yet looked at.

## Method

PE headers and import tables read with `pefile`: machine type, link timestamp, image base, ASLR
flag, section names, sizes and entropy. Then a case-insensitive search of each binary for renderer
DLL names (`d3d9`, `d3d11`, `d3d12`, `dxgi`, `vulkan-1`, `opengl32`), headset runtimes (`openvr`,
`openxr`, `oculus`), protection markers (`denuvo`, `securom`, `.bind`) and middleware names, with
readable strings pulled around the interesting hits. A string match shows a name is present in the
file, not that the code path is used. A `.text` section with entropy near 8.0 is encrypted or
compressed, not normal code.

## Risks noted

- ⚠️ The Steam DRM wrapper encrypts the code on disk, so static reading of the code needs it unwrapped first (Steamless, a public tool, is the usual route) `[hypothesis]`.
- ⚠️ **Heavy Rain is played almost entirely through fixed, film-style cameras.** A head-tracked first-person view is not how this game is built, so the realistic first goal is probably a large 3D screen in the headset rather than being inside the scene `[hypothesis]`.

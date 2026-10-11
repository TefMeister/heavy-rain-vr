# 2026-10-11 reader: recipe for our proxy to switch the built-in free camera on

From: the static reader helper of a live `/lm` session, dev PC. Read from a Steamless-unwrapped copy on E: only.
Nothing in the game folder, nothing run. Addresses are RVAs from image base `0x140000000`. The class names come
from the game's own RTTI, recovered with ghidrust.

## The call chain (all x64 Microsoft calling convention: rcx, rdx, r8, r9)

| RVA | What it is | Signature (unique in the unwrapped image) |
| --- | --- | --- |
| `0x263B10` | **`MakeFreeCam(viewport, int index)`**, the native function behind Lua `ViewportMakeFreeCam` (the Lua wrapper is at `0x270050`) | `40 57 48 83 EC 30 48 C7 44 24 20 FE FF FF FF 48 89 5C 24 48 8B DA 48 8B 49 58` |
| `0x263C50` | **`DisableFreeCam(viewport, int index)`** (Lua wrapper at `0x270100`) | the start is not unique (4 hits). Use `80 B8 A1 00 00 00 00 74 52 C6 80 A1 00 00 00 00 4C 8B 88 F8 01 00 00` (unique), then function start = hit − `0x6B` |
| `0x2673F0` | **`GetCameraDirector(viewport, int index)`** returns a `CAMERA_DIRECTOR*` or null. It has 37 call sites, including gameplay code | `48 89 5C 24 08 57 48 83 EC 20 48 8B D9 8B FA 48 8B 49 58 48 85 C9 74 34` |
| `0x291490` | **`SetFreeCam(director, bool on)`**, used by the debug menu's "Free camera" toggle | `48 89 5C 24 08 57 48 83 EC 20 0F B6 FA 48 8B D9 38 91 A1 00` |
| `0x291520` | `PlaceFreeCam(director, director+0x230)`, which the menu calls right after switching it on | `40 53 48 83 EC 20 4C 8B 89 F8 01 00 00 48 8B DA` |

All of the above is `[inferred-static 2026-10-11]`.

- **The index is 1 for the main view.** The debug menu always passes 1 (`0x2912C8`, `0x2900DE`). Gameplay code passes a stored per-object index (`[obj+0x1F0]`) `[inferred-static 2026-10-11]`.
- **The viewport** is resolved from handle `owner+0x168` by `0x225490` `[inferred-static 2026-10-11]`.
- **There is no global pointer.** I found no static global for the viewport or the director.
  - Cheapest capture: detour `GetCameraDirector` (`0x2673F0`) and keep `rcx` whenever `edx == 1`.
  - That detour runs on the game-logic thread, so it is also the safe place to make the toggle call [hypothesis].

## CAMERA_DIRECTOR layout (vtable RVA `0xCEDCE8`)

- `+0x90` int: the slot passed to `Activate`.
- `+0xA1` byte: **free camera on**.
- `+0x1F8` handle: the "Integrated FreeCamera" object, class `CAMERA_BEHAVIOR_FREE`, vtable RVA `0xCF1A90`.
  - Handles resolve as: `+0x30 & 0x202000` set and `+0x50` non-null, otherwise through `0xAC2F30` (that path may load things).
- `+0x230`, `+0x2E0`, `+0x390`: three 0xB0-byte camera-parameter blocks.

All `[inferred-static 2026-10-11]`.

Switching on means: flag=1, `Activate(freecam, dir+0x90)` (`0x329CE0`), then `freecam->vt[0x2E8](dir+0x230)` copies
the current shot into it. Switching off calls `freecam->vt[0x2E0]` (`0x329DB0`) `[inferred-static 2026-10-11]`.

## Moving it

- The free behaviour's per-frame update is vt+0x298 = `0x3E24D0`. Its input handler is vt+0x2D0 = `0x3E1F00` [inferred-static 2026-10-11].
- It works from the `FreeCam_*` actions, registered by ID `0x1F` and up in `0x3E3160`. Whether the PC build binds keys to them is unknown [hypothesis].
- The update writes a block of floats at `freecam+0x224…+0x278`, plus `+0x360…+0x36C`. That is probably its pose, and it is the place to write a head pose [hypothesis].
- Next step: log those floats live while the camera moves.

## Threads

Do **not** call these from the Present hook. They change camera-behaviour state that the game thread reads, and handle
resolution can load objects [hypothesis]. Set a flag in Present and do the call inside the `GetCameraDirector` detour.

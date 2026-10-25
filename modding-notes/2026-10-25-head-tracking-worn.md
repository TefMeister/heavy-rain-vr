# 2026-10-25 — head tracking in the real headset (home PC)

- Bedroom scene, free camera on by trigger file, then `heavyrain_freecam_xr.txt`. Log: PrivateCppRuntime on (14.51),
  session running, recentred, head yaw / pitch / roll followed at 72 poses a second `[verified-live 2026-10-25, n=1]`.
- Tefa: "game is on and i can look around on the monitor, but inside the headset it's black". Black is this build's design:
  `freecam_xr.c` sends empty frames (no layers), so the head drives the game camera and nothing is shown in the headset.

## Next
- The picture into the headset: one swapchain per eye, the back buffer copied in and shown as a projection layer at the
  pose it was drawn from (Manhunt's `mhxr_xr.c` and Metro's bridge to lift from); one flat picture first, stereo after.

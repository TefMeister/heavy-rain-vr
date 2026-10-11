# 2026-10-11 — `/pd` (dev PC): a head pose laid on top of the free camera, without making it spin

**The game was not launched, and nothing here has been run in it.**

## What the game does `[inferred-static 2026-10-11]`

The free camera's per-frame update (`CAMERA_BEHAVIOR_FREE` vtable +0x2D0, RVA `0x3E1F00`) keeps no separate yaw or
pitch. It moves the position along the rows of its own matrix at `+0xF0` and then multiplies the rotation **in place**.
That matrix is the camera's only state. So a head pose written straight into it would be carried into the next frame
and add up: the view would spin. The update is reached only through that one vtable slot (one pointer to it in the
whole image, no direct calls).

## What was built `[compile-verified 2026-10-11]`

`staging/heavy-rain-vr/proxy-d3d11/hooks/freecam_pose.c`, wrapped around the update through that vtable slot (the slot
is checked to hold the expected function before it is swapped):

1. Before the update: if the matrix still holds exactly what we wrote last frame, put the game's own back. If anything
   else changed it in between (a reset, "look at player"), keep theirs.
2. The game's update runs on its own, clean state.
3. After: keep a copy of the game's result, then write it back with the head pose on top
   (yaw about up, pitch about right, roll about back, plus a camera-relative offset).

The head pose comes from `heavyrain_freecam_look.txt` next to the exe (`yaw pitch roll x y z`, degrees and world
units), read four times a second, until a headset feeds it. The game's own pose (rows, position, FOV) and four
counters (updates, head written, restored, kept theirs) are logged at most twice a second while the camera is on.

## How it was checked

- Self-test 33/33 (12 new) against a stand-in update that, like the game's, changes the matrix in place: over 30
  frames with a head pose on, the game's own state matches an untouched reference exactly, and every frame shows that
  reference with the head pose on top `[verified-numerically 2026-10-11]`.
- **The test can fail:** with step 1 removed, the same test reports a 2.3 drift and fails three checks.
- The old pose logger (`+0x224`, `+0x360`), disproved live earlier today, was removed (`proxy-d3d11/archive/README.md`).
- The build was not reproducible (time stamp in the file); `-Wl,--no-insert-timestamp` added, now byte-identical
  across builds. Deployed `cab5b4db065f`, previous kept as `d3d11.dll.bak-2026-10-11-pd-pre-pose`, stamped.

## What is NOT established

- That the caller copies the returned block after the update, so the picture uses our written matrix `[hypothesis]`.
  If it copies before, the head pose shows one frame late, or not at all.
- The sign conventions (which way a positive yaw turns) and the world unit.

## The next run (`[FLAT]`, one launch)

CONTINUE into the bedroom, switch the free camera on (`heavyrain_freecam_on.txt`), then:

1. Read the log's `pose (game's own)` lines while flying with W and the arrows: the rows and position should change.
2. Drop `heavyrain_freecam_look.txt` containing `15 0 0 0 0 0`, wait 5 s, remove it.

| result | means |
| --- | --- |
| the view turns about 15° and holds still, then turns back when the file goes | ✅ the head-pose layer works |
| the view keeps turning while the file is there | the restore misses: read the `restored` / `kept theirs` counters |
| nothing turns, `head written` climbs | the caller copies the pose before our write: move the write to the caller |
| no `pose:` lines at all | the vtable slot was not the expected one: read the `pose:` install line |

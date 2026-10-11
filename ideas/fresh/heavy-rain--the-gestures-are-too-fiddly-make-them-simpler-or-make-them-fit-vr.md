# The gestures are too fiddly: make them simpler, or make them fit VR

Order: 18000
From: the ideas repo, `games/heavy-rain.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/heavy-rain.md>), copied 2026-10-11

`[raw]` · `[not judged]` — ⚠️ **not checked against the game**

> "heavy rain needs a whole new way of input i think, it is very tricky adn gesture based"
>
> "what i meant is that right now the gesture based interaction is very complicated and we need to either make it
> simpler or adapt to vr"

Almost every action in Heavy Rain is a gesture: hold a button and move the mouse along the drawn path to open a door,
shave, brush teeth, fight. As it stands that is complicated and easy to fail. Two ways out, either or both:

- **Simpler:** the same prompt, but one easy action does it (a press, or a short movement in roughly the right
  direction), so the game no longer asks for exact paths.
- **Adapted to VR:** the hands do the real movement instead (reach out and pull the door, swing the arm for a punch),
  with the motion controllers standing in for the mouse movement the game asks for.

**What it'd take:** for both, read which gesture the game is waiting for (the on-screen prompt or the game's own
input state), then either answer it for the player (simpler) or turn the controller's real movement into the mouse
or stick movement it expects (VR). The game's input actions are registered by name in the exe, which may help.
⚠️ Not checked: how the game reads gestures has not been looked at.

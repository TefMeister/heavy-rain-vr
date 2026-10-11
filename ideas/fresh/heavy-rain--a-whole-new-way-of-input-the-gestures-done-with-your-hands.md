# A whole new way of input: the gestures done with your hands

Order: 18000
From: the ideas repo, `games/heavy-rain.md` (<https://github.com/TefMeister/mod-ideas/blob/main/games/heavy-rain.md>), copied 2026-10-11

`[raw]` · `[not judged]` — ⚠️ **not checked against the game**

> "heavy rain needs a whole new way of input i think, it is very tricky adn gesture based"

Almost every action in Heavy Rain is a gesture: hold a button and move the mouse in the drawn direction to open a
door, shave, brush teeth, fight. On a flat screen that is fiddly; in VR the same moves could be done with the hands —
reach out and pull the door, swing the arm for a punch — with the motion controllers standing in for the mouse
movement the game asks for.

**What it'd take:** read which gesture the game is asking for (the on-screen prompt, or the game's own input state),
and turn the controller's real movement into the mouse or stick movement it expects. The game's own input actions
are registered by name in the exe, which may help. ⚠️ Not checked: how the game reads gestures has not been looked at.

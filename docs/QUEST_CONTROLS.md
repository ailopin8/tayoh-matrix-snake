# Quest controller controls — v0.11

Open https://ailopin8.github.io/tayoh-matrix-snake/ in the Quest Browser and choose Enter VR. Entering VR starts paused. Wake both controllers. The in-world status shows detected hands and matrix size; the guide appears above the matrix.

| Control | Action |
| --- | --- |
| Right A | Run / pause |
| Right B | Pause, then request one simulation tick (ignored while another request is finishing) |
| Left X | Next display lens; disables automatic lens switching |
| Left Y | Show / hide controller help |
| Either index trigger (L2/R2 equivalent) | Aim ray and release to select a console button or inspect a cell |
| Either side grip (L1/R1 equivalent) | Hold to grab the matrix; move to pull, turn your wrist to rotate |
| Both side grips | Move hands together to translate; spread / close hands to resize; turn the line between hands to rotate |
| Left stick | Move matrix sideways / forward-back in reference-space axes |
| Left stick click | Toggle forward-back versus up-down movement |
| Right stick | Continuous yaw / pitch rotation |
| Right trigger + right stick | Up enlarges, down shrinks; left/right rolls the matrix. Suppresses ray selection for that gesture |
| Right stick click | Restore original position, orientation and 1× size; simulation state stays intact |

Matrix size is bounded to 0.25–4×; reference-space position is bounded to x ±5 m, y −2…5 m, z −8…2 m. These are presentation bounds, not locomotion. Use right stick click if the matrix leaves your view. The console remains fixed, so it does not spin or shrink with the matrix. World coordinates, energy/material ledgers and authoritative Python state are independent of presentation transforms. No inertial spinning is applied after release.

The support console button still requires a second confirmation before queuing an intervention. Meta/system/menu buttons are not assigned. Hand tracking without controller gamepads is not supported by these shortcuts; ray selection remains available where WebXR emits select events.

## Input contract

Input is sampled from each XRInputSource.gamepad per XR frame, keyed by source identity and handedness, never array position. Face shortcuts are enabled for meta-quest-touch* and oculus-touch* profiles only; standard mapped controllers retain stick/grip handling. xr-standard uses trigger 0, squeeze 1, stick click 3, stick axes 2/3. Quest profiles map A/X to button 4 and B/Y to button 5. New sources seed button state, so an already held face button does not fire. Button actions use rising edges, stick deadzone is 0.18, dt is capped at 50 ms. Grabs rebase when the tracked source set changes and release on lost tracking. Hidden sessions pause simulation and clear input state; exiting pauses too.

One-hand transforms use current grip pose × inverse initial grip pose applied to the starting world transform. Two-hand transforms use the hand midpoint, distance ratio and quaternion aligning the initial hand separation to the current separation. Two-hand twist about that separation is ambiguous; use right-trigger stick roll or a single wrist grip for that degree of freedom.

Sources: [W3C WebXR Gamepads mapping](https://www.w3.org/TR/webxr-gamepads-module-1/), [Immersive Web Quest Touch Plus profile](https://github.com/immersive-web/webxr-input-profiles/blob/main/packages/registry/profiles/meta/meta-quest-touch-plus.json). No controller artwork or third-party interaction implementation copied.

## Verification limits

Automated synthetic input tests exercise production mapping and transformation code. They do not prove physical Quest tracking, browser profile exposure, ray targeting accuracy, controller ergonomics, or headset frame rate. Those require a physical Quest 3S check. In headset: A run/pause; B increments once; X cycles; Y hides/shows help; aim/release all console buttons; inspect a moving cell; drag/rotate one grip; resize/rotate two grips; release one without a jump; test all stick modes and home; hide/resume and reconnect controllers. Confirm size/status feedback and that view manipulation leaves the state hash unchanged while paused.

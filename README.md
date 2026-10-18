# TAYOH Matrix Snake 0.9

Two snakes (green A and blue B) compete for one shared pool of food and special resources. Each senses the other and uses a bounded model to avoid its body, anticipate its next step and discount contested food. Shared-cell claims use alternating right-of-way; this prevents double consumption, not unequal outcomes.

A deterministic Python systems-game prototype with a 10×10×10 world, interactive desktop slices, full-cube preview, shared-state WebXR presentation, and a boundary/compression laboratory.

## Protector / Healer / Child

The boundary is the protector, the food-producing process and its timed food are the healer, and the snakes are children. Six boundary faces take seeded uncertain damage and use reserve to repair. Expired food feeds the protector; consumed food feeds children, who return energy to healer and boundary. Safe conditions sustain production. New information and boundary conditions can generate regular, enriched or toxic food. Every role holds bounded models of every other role.

The role panel accepts labeled stress, support or information mapped to intensity 0–10. Queue an observation, Step or Run, inspect/export the outcome, and use it to frame another experiment. The adapter is explicit: translating a real domain into these roles and numbers remains a modeling choice requiring validation.

Read `docs/SYSTEMS_FRAMEWORK.md` for the authoritative v0.8 rules, reciprocity, uncertainty, input schema and revised energy/material ledgers. `docs/MATHEMATICS.md` retains the underlying spatial, diffusion and competition mathematics.

## Open on Quest via GitHub Pages

The publishing build runs this same Python engine inside Quest Browser with Pyodide. It is self-contained: the laptop server does not need to stay running. Each browser tab has an independent world; it is not synchronized with the laptop or other tabs. Wait for Python to load, then select Enter VR. Details and publication instructions: `docs/GITHUB_PAGES.md`.

## Start locally

Python 3.10+ and a modern WebGL browser are required. For laptop-server mode, no package installation, build step, CDN access, or Python dependencies are needed.

```sh
cd tayoh-matrix-snake
python3 server.py
```

Open http://127.0.0.1:8765 . Autonomous A is enabled by default; B always forages autonomously. Press Run to watch both snakes seek and consume food, or Step to inspect one decision. Uncheck Autonomous A to steer manually or buy skills. Food production now depends on boundary/healer/child viability; uneaten food expires into protector upkeep. Special resources renew under viable boundary conditions; current resource desirability and reasons appear in the interface. Choose a direction with the buttons or arrows (X/Y), Q/E (Z). Inspect any of 30 axis slices and click cells for exact values. Drag the spatial view to orbit; scroll to zoom. Skills cost 12 battery GU from A in manual mode. Growth is capped at 24 segments per snake; excess structure enters compost. Battery capacity and digestion improve with food milestones within explicit bounds. There is no final score, but survival is not guaranteed. Reset returns to seed 42. The server is the only simulation authority; other browser tabs share the world. Use one Run clock to avoid competing browser action submissions. Each world tick advances both snakes.

```sh
python3 -m unittest discover -s tests -v
python3 replay.py replay.json
```

Export replay downloads the seed, snake count, systems mode, queued inputs and accepted live-step actions; the replay utility prints the final state hash. Reset starts a new history. Python runtime/code version should match for durable deterministic replay.

## Headset use

For PC-attached headsets, open the localhost URL in a compatible WebXR browser and press Run, then Enter VR. For a standalone headset, expose the Python service through a **trusted HTTPS reverse proxy** that forwards both static files and `/api/*` to the same service. The headset's localhost refers to the headset, not your laptop. Plain HTTP at the laptop's LAN address generally does not meet WebXR secure-context requirements. The GitHub Pages build instead runs Python in the headset browser; it uses no server-side Python.

The service binds loopback by default. It is a local development tool with no accounts or authentication; do not expose it as a public production service. Configure any remote proxy for your own restricted access. `--host` and `--port` are optional local hosting settings.

One click requests a browser immersive session when supported; browser consent may still be required. It shows the same authoritative cube, not a second simulation. Controller trigger/select cycles world directions in manual mode; autonomous mode chooses its own direction. Enable Run before entry; choose a fresh reset if the snake has died. There is no headset HUD. Physical headset entry, stereo, tracking, controller mapping, HTTPS remote use, and performance have not been verified on hardware; see docs/VERIFICATION.md.

## Files

- `engine.py`: deterministic transition, state snapshots, finite recursive models, boundary functions.
- `systems.py`: protector/healer/child dynamics, timed food, uncertainty, reciprocal models and input/output adapter.
- `resources.py`: seven resource types and their explicit effects.
- `server.py`: standard-library HTTP service, read state/replay/output, tick-checked actions, inputs and reset.
- `web/`: desktop and WebXR interface, vendored Three.js and license.
- `docs/MATHEMATICS.md`: exact equations, ordering, invariants, philosophy, limitations, sources.
- `tests/`: engine and HTTP integration checks.
- `replay.py`: action log replay and checksum.

The boundary demonstration is inspired by the supplied red/blue folding images. It explicitly uses a many-to-one max-norm map; it is not a proof that an arbitrary fold and a single cut make a closed boundary. Its controls are independent of the snake world.

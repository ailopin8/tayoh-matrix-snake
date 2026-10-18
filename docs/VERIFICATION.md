# Verification — 19 October 2026 — v0.8

## Checks

56 Python unittest cases pass. Fourteen original systems-role cases plus an arrival/deadline case cover role initialization, protector consumption at food expiry, child intake and reciprocal transfer, unsafe-space production pause, child-safety gating, support/information encoding, stress-dependent toxic production, transit avoidance of toxins, input validation atomicity, input-inclusive replay, bounded models that affect production, boundary failure propagation, energy/material accounting and food metadata consistency over 180 ticks, independent snapshots, and arrival during the final available food tick. Two HTTP cases cover input/output/replay and rejection of invalid input. The 39 previous focused engine, autonomy, competition and HTTP cases remain in place. Legacy ecology fixtures explicitly use systems=False; default HTTP and new role cases use the coupled framework.

Python compilation and JavaScript syntax checks pass. A real Chromium smoke check confirms four role meters, 100 slice cells, reciprocal role-model display, queued labeled observation, next-tick application, and provenance present in /api/output. Desktop screenshot saved as output/playwright/systems.png. The last planner adjustment (arrival at n+d−1) is covered by the focused deadline test.

## Finite experiments before the final deadline refinement

Two 300-tick seed-42 runs checked exact energy and material ledgers each tick:

| Scenario | Protector integrity / healer vitality at tick 300 | Protector food consumed | A food / B food | Children |
|---|---|---|---|---|
| Baseline | 100 / 100 | 150 | 99 / 103 | both alive |
| Initial stress 10 and information 10 | 100 / 100 | 143 | 105 / 106 | both alive |

The stressed run recovered by the end; these endpoint observations do not imply disturbance had no transient effect or that every stress schedule is survivable. The numbers are historical experiment results for the implementation immediately before the conservative deadline exclusion was refined to admit a reachable final-tick food. The final regression suite, rather than these exact counts, verifies the packaged implementation. No eternal-survival claim is made.

## Accounting checked

For two children: shared energy + child batteries/heat + protector/healer reserves/heat = 20,320 + cumulative external energy supply. Live food + body segments + compost = 86 + supplied food material. Protector-expired food, role upkeep, repair, support and reciprocal contributions are included. Food chemical energy is recognized at intake, not stored as a measured physical property in a food particle.

## Interpretation and hardware limits

Role identity, thresholds, uncertain damage envelope, viability summaries and input normalization are explicit designed assumptions. They have not been calibrated to an external scientific or organizational system. The typed adapter cannot automatically infer an arbitrary real system's causal structure. Uncertainty is seeded and bounded; its external cause remains unidentified.

Physical WebXR headset entry, stereo, tracking, controller mapping, comfort/performance and standalone trusted-HTTPS use remain untested. Desktop and VR use the same cube snapshot; role-panel forms and meters are desktop UI, not an immersive headset HUD. The cube outline and food colors carry the role-state cues into the spatial view. Use one client Run clock during reproducible experiments.

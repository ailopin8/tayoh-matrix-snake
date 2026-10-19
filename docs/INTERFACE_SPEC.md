# Adaptive interface specification — 0.10

## Components and tokens

| Component | Input / state | Behavior |
|---|---|---|
| Declaration | purpose≤120, inclusion/exclusion/question≤180 characters | Local browser interpretation; persist on the origin; no engine mutation |
| Attention policy | snapshot + task + automatic/pinned lens | Pure state reducer; mode, focus, lens, explanation and urgent text |
| Relation summary | system counters and conditions | Six typed directed descriptions; no mixing unlike units |
| Input review | validated label, channel, integer 0–10, optional x/y/z | Draft only; explicit second action queues; editing fields cancels old review |
| Comparison | baseline at queue + next matching applied label | Reports boundary, pressure and food differences; not causal attribution |
| View journal | context, policy, history, baseline, outcome, state hash | Local JSON download; separate from engine replay |
| Spatial console | authoritative snapshot + presentation description | Fixed panels, ray-selectable controls, cell inspection; no simulation ownership |

Semantic tokens: `--role-protector` #72dfc5, `--role-healer` #ffd17a, `--role-child` #83b8ff, `--attention` #ffad83. Spacing: 8/16/24px. Labels and words accompany color. Existing simulation colors remain distinct. Focus outline is 3px with 3px offset. Most interactive fields retain native label/keyboard semantics; details reveal model/code quantities on request.

## Layout and spatial units

Desktop declaration is two columns; below 700px it becomes one. Relationship cards wrap at 260px minimum. The spatial canvas is 520px high (460px below 700px). Stable Run/Step/VR controls precede the declaration. Auto adaptation changes lens and text, not document section order or camera position.

The cube retains one-meter width at world center (0,1.3,−2). The spatial banner is 1.65×0.25m, local (0,0.88,0). Role panels are 0.72×0.30m at local (−0.93,0.36,0), (−0.93,−0.1,0), (0.93,−0.1,0). Six action panels are 0.31×0.16m, local x=−0.85+0.34i, y=−0.78. These are design starting values, not verified comfort specifications. Canvas text is capped to fit; complete text remains available in desktop controls/journal. No head-locked HUD or involuntary locomotion is introduced.

## States and errors

- Loading: show Python loading message; no synthetic live world.
- Observation/recovery/stabilization: show rationale, active lens and urgent alert when applicable.
- Manual lens: pin it, retain critical text, make the automatic checkbox state explicit.
- Review: show exact input label, channel, address and immediate encoding effect. No tick/queue mutation yet.
- Cancel: discard review only; no attempt to erase queued inputs.
- Apply: expected-tick validation; a busy or stale step can require retry. Do not claim success on an error.
- Applied: show observed before/after deltas; label other concurrent processes.
- Failure: keep world and outcome inspectable, retain Reset as an explicit action.
- VR unsupported: disable Enter VR with text. Exit is also available through the headset system interface.

A reviewer should inspect double-click/late input races, long text, paused recovery, pinned-critical alerts, empty coordinates, changed fields after review, and runtime loading failure. An input canceled while hashing cannot become a later actionable draft. Input data is handled as text/JSON and never compiled into code.

## Interaction adapters

Native DOM controls provide keyboard and assistive-technology semantics on desktop. Desktop pointer raycasts mirror spatial button/cell selection; movement over five pixels is treated as orbit rather than activation. Each of two XR controllers supplies its own world ray on select-start. A control hit takes precedence over cell inspection. No hover or dwell injects an input.

The immersive input experiment is intentionally narrow: Support +2 is reviewed then confirmed at the same location. Full text input, coordinate forms and purpose editing remain desktop capabilities. Changes in purpose affect presentation only, so users do not accidentally alter the equations through interface wording.

## Acceptance checks

Automated: pure policy priorities, immediate urgency, five-tick recovery hold, pinned critical alerts, failure review, draft validation/copying, typed relations and no mutation of simulation snapshots. Native engine suite stays unchanged.

Desktop: load browser Python, change task/lens without advancing tick, review without queueing, cancel, apply and verify queued count, Step and see provenance/comparison, inspect cells, check color-independent labels and capture the spatial console.

Headset still required: both controllers' target accuracy, ray collisions at panel edges, review/confirm distinction, exit behavior, readable angular text size, panel comfort at seated/standing heights, frame rate with energy overlay, and safe interaction under evolving critical states. Until these pass, controller support is implemented but unverified on hardware.

## v0.13 simple workspace

Default desktop layout: Run / Step / Enter VR; matrix with Home, turn and size buttons; a relationship path and four component selectors; three input presets (support, stress, information at intensity 2). Presets use the existing reviewed-input pipeline: preview, explicit confirmation, next authoritative tick. Session options contain reset, autonomy and replay export. Advanced tools retain declarations, raw models, slice explorer, custom inputs, resource catalog and compression lab. Existing IDs and state contracts are preserved.

Component explanations use actual systems.models estimates and Python purpose evidence. They describe smoothed role-viability beliefs, including self and the boundary, rather than claiming a complete representation of the world. The relationship path is a schematic of designed exchanges, not live causal proof. The interface does not turn declarations into physics.

VR uses a short running/paused banner, one component explanation card, simulation buttons and a Next part ray button. Detailed role cards and schematic arrows are hidden; controller help starts hidden and Y reveals it. Controller actions, matrix transforms and input review semantics are retained. Desktop 3D hides the spatial text console, leaving an uncluttered matrix; its HTML controls remain available.

Verification: 24 JavaScript tests pass. Browser checks cover selecting a component, reviewing support, confirming it and stepping. Existing Python engine is unchanged. Physical headset readability and reachability require Quest testing.

# Interface philosophy for a bounded systems matrix

TAYOH 0.10 · 19 October 2026

## The central proposition

**Make purpose, boundary, relationships and uncertainty inspectable; adapt attention to the current need while preserving the observer's control.**

The interface is the place where a person declares a model, observes its consequences and decides what to ask next. A cube is a useful bounded address space; its shape alone is not a theory of the system placed inside it. The interface must explain what its cells mean, what the boundary excludes, what counts as viability, and how an observation becomes an intervention.

The protector/healer/child triad is our proposed relational grammar. It is not presented as a finding that every real system naturally has exactly three roles. Applying it to another domain requires justifying the mapping, choosing quantities and validating the rules. A domain that does not fit should expose that mismatch rather than be forced into a persuasive picture.

## Philosophical commitments

### 1. A boundary is both an operational constraint and a declared modeling choice

The operational boundary limits movement, exchange and existence in this prototype. The declared boundary identifies what the observer includes, excludes or treats as uncertain. These are related, but editing the declaration does not silently change the operational rules.

The interface therefore places **Included within the boundary** beside **Outside / uncertain**. This keeps exclusions visible. The unknown is represented by a stated envelope and provenance rather than an invented entity. A coordinate identifies a location in the model; it does not make a label into a physical measurement.

### 2. Purpose selects questions before it selects answers

A purpose provides a criterion for noticing change. “Understand reciprocal viability,” “maintain viability,” and “test an input” imply different immediate questions. They should not require three unrelated applications or silently invoke three different mathematical worlds.

The declaration and current-task selector change interface attention. The current engine's survival objectives, thresholds and dimensions remain explicit code. A future rule editor needs its own schema, preview, validation and replay contract; it cannot be replaced by interpreting a sentence as executable truth.

### 3. Roles are relational purposes, not isolated objects

Protector, healer and child are useful because each depends on what the others provide. The interface should show **who provides what, under which condition, with what cost or delay**. A condition such as safe production must not be drawn or added up as though it were an energy quantity.

The relationship view consequently distinguishes conditions, energy contributions, material intake and information trails. It shows the relationship before exposing the implementation tables. A damaged boundary draws attention to protection and repair; unsafe production draws attention to food availability and deadlines; a depleted child draws attention to reachable nutrition and competition.

### 4. A model is a perspective with a timestamp

Actual state, sensed state, an estimate, a prediction and an unidentified cause are different categories. The role tables contain bounded estimates; the snakes' next-head hypotheses can be wrong. The interface should let a person inspect those distinctions without suggesting an omniscient recursive intelligence.

Every model has an observation phase. Deeper inspection is available on request. A future partial-observation system would need to show missing information rather than fill it with confident graphics.

### 5. Intervention is a visible commitment

An observation does not specify its own encoding. Someone chooses whether it means stress, support or new information, selects a scale, and chooses or accepts a matrix location. This process can lose information.

An input must therefore pass through **review → explicit queue → applied tick → observed outcome**. The review names the input, channel, intensity, cell and immediate encoded effect. It does not predict a guaranteed downstream outcome. Canceling a review makes no simulation change. A queued input is already part of the experiment history; canceling a later review does not erase it.

### 6. Adaptation should explain itself

The system can direct attention without taking over the observer's purpose. It may change the active lens when a viability threshold is breached, but it must explain the reason and retain a history. A person can pin a lens, while urgent conditions remain visible in words.

The interface does not move the camera, teleport the observer or rearrange essential controls when a need changes. It changes the relevant evidence and emphasis. Dynamic meaning does not require constantly moving furniture.

### 7. Outcome is evidence for another question

A change after an input is an observation. Diffusion, resource renewal, competition, uncertainty and other queued events may have changed the same quantities. The comparison panel reports an observed before/after difference and explicitly avoids labeling it an isolated causal effect.

The next question can challenge a boundary, input scale, role assignment, threshold or purpose—not merely ask for another dose of the same intervention. The view journal preserves the declaration and attention history alongside a state hash and outcome. Engine replay preserves computational actions; the view journal preserves part of the observer's interpretation. Neither is a complete record of a real external system.

## Research foundations and what we infer from them

These sources informed the design; the TAYOH rules and thresholds below are our proposals, not claims made by those authors.

- **System goals and information flows:** Meadows discusses places to intervene, including information flows, rules and goals. We infer that an interface should make its purpose and intervention level explicit instead of presenting every action as an undifferentiated button. [Donella Meadows, Leverage Points](https://donellameadows.org/archives/leverage-points-places-to-intervene-in-a-system/)
- **Visibility of status:** Nielsen Norman Group argues that feedback should keep users informed about system state. We apply that principle to queued/applied input states, an attention rationale and source-aware role meters. [NN/g, Visibility of System Status](https://www.nngroup.com/articles/visibility-system-status/)
- **Spatial comfort:** Microsoft advises stable spatial content, limiting uncomfortable near/depth changes and avoiding unrequested self-motion. We use fixed world-anchored panels around the matrix, with no automatic camera movement. Their device-specific distances are not treated as a validated Quest 3S calibration. [Microsoft, Comfort](https://learn.microsoft.com/en-us/windows/mixed-reality/design/comfort)
- **Progressive disclosure:** Microsoft's gaze/dwell guidance includes progressive disclosure and interaction stability. We apply disclosure through an overview, optional model inspection and explicit input review. The implementation uses trigger selection, not automatic dwell activation. [Microsoft, Head-gaze and dwell](https://learn.microsoft.com/en-us/windows/mixed-reality/design/gaze-and-dwell-head)

## GitHub pattern study

The exact repository snapshots consulted are retained in `design-source-snapshots.json`. We adopted patterns, not their source code, APIs or dependencies. Existing Three.js remains the renderer.

| Repository / inspected material | Observed pattern | TAYOH adaptation and deliberate limit |
|---|---|---|
| [pmndrs/uikit](https://github.com/pmndrs/uikit/blob/099f6f701c5fbec356f9f2d5d7dc86c8a6ff2cbf/README.md) | Composable spatial UI for Three.js, including a vanilla path | Stable, reusable role panels and a consistent action row; no migration to its component runtime |
| [pmndrs/xr UI example](https://github.com/pmndrs/xr/blob/0e1acd868ca744032240db819d1e428bd1812901/examples/uikit/app.tsx) | Explicit container layout, semantic controls, scrolling content and adjustable panels | Separate overview from detail and keep control meanings visible; do not introduce resizable floating windows that undermine this prototype's stable map |
| [Meta Immersive Web SDK](https://github.com/facebook/immersive-web-sdk/tree/0778f518db51e9d1836977f3b6fed9b53f3f0c6f) | A WebXR framework that organizes interactions and spatial UI on Three.js | Separate the spatial interaction adapter from simulation and presentation policy; retain the existing small renderer rather than replace the app with a new SDK |
| [XState](https://github.com/statelyai/xstate/tree/6a85c4057dc7c0906381664249e0b1bac300cd92) | Explicit statecharts/actors describe reactive application behavior | A small, pure presentation-state policy with guards, urgency, recovery hold and a manual override; this does not use or claim to implement the full XState runtime |

No repository's design is evidence that our systems theory is universally valid. These are engineering precedents for making interactions legible and maintainable.

## The interaction grammar

**Declare → Bound → Relate → Observe → Review → Apply → Compare → Revise.**

1. Declare a purpose and a question.
2. Name the included system and the uncertain/external domain.
3. Inspect dependencies and distinguish their exchange types.
4. Inspect actual state, model estimates and time/deadlines through an appropriate lens.
5. Review a labeled, scaled input and its address/effect before committing it.
6. Queue it and advance the authoritative simulation.
7. Compare outcomes with the recorded baseline; retain uncertainty and other changing processes.
8. Revise the declaration or experiment, and preserve the view journal if it matters.

The cycle can begin with observation of an existing world; it does not force a form-filling ritual before every action. The declaration is always revisable. Pause, Step, lens choice, input cancellation and immersive exit occupy stable control locations.

## Implemented adaptive states

The UI policy reads a snapshot and returns a presentation description. It never changes the Python state. Priorities are designed thresholds for this prototype:

| Condition, in priority order | Attention state | Default lens / focus |
|---|---|---|
| World stopped or protector failed | Review | Boundary / protector |
| Boundary integrity <50 | Stabilize | Boundary / protector |
| Healer safety condition false | Stabilize | Material / healer |
| Any child <25% battery | Stabilize | Material / children |
| External pressure ≥5 | Investigate | Boundary / protector |
| Task is testing or input is queued | Experiment | Information / relationships |
| Task is maintaining | Maintain | Relationships |
| Otherwise | Observe | Relationships |

Urgency takes effect immediately. Nonurgent changes wait until five logical ticks have passed since the last urgent observation or relevant entry time. This hold reduces rapid attention switching; while the simulation is paused, automatic recovery does not use wall-clock time. Explicit task/lens/automatic changes are user events and reevaluate immediately. Manual lens pinning leaves urgent text visible. Mode/lens transitions are recorded with their reason; the last twelve are displayed.

This is attention allocation, not automatic remediation. A red boundary does not secretly inject support. A new task does not silently change the children's policy.

## Spatial vocabulary

The cube is the computational place. Fixed panels identify the protector, healer and children, and show their relevant quantities. The three schematic arrows in the overview provide orientation; the full desktop relationship list supplies typed directions and measured counters. A schematic arrow is not a quantified energy stream.

Five lenses preserve the same coordinates:

- **Relationships:** entities, three schematic arrows, role cards and reciprocal summaries.
- **Boundary:** the integrity-colored boundary and protector emphasis; entities remain for context.
- **Energy:** an instanced field overlay whose brightness/size reflects cell energy; structural entities remain visible.
- **Material:** bodies, food and special resources, with signal-only markers hidden.
- **Information:** trails and bodies, with food/resource markers hidden; critical status is retained outside the cube.

Inspecting a cell identifies coordinates, tick and E/M/I without injecting information. A yellow outline identifies the selected cell. Layer and lens selection never change spatial addresses. The default scene is still a tabletop-scale matrix, not a forced first-person snake camera.

## What is implemented and what remains a design proposal

Implemented: editable declaration, task/lens control, adaptive attention and rationale, manual pinning, typed relationship summaries, explicit input review and cancellation, optional coordinates, before/after observation, exported view journal, five rendering lenses, world-anchored role/attention panels, two controller-ray adapters, cell inspection and a fixed action row.

The VR row provides Run/Pause, Step, Next lens, a two-activation Support +2 experiment, Cancel draft and Exit VR. Support +2 encodes 16 GU and a pressure reduction up to two; its first activation shows the review, its second queues it. Full purpose editing and arbitrary typed observations remain desktop/browser-form interactions. Trigger input now selects the ray-targeted control or visible cell; it no longer cycles manual snake directions. Manual snake steering remains available through the desktop controls.

Not implemented: natural-language rule synthesis, arbitrary external-data import/calibration, rule editing, causal identification, eye-tracking, hand-tracking, spatial audio, headset screen-reader semantics, in-headset text entry, or full counterfactual branch comparison. Physical controller interaction, readability, comfort and frame rate require Quest 3S hardware testing. Desktop rendering and pure policy tests cannot validate them.

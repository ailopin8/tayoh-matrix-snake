# Protector / Healer / Child — a systems computing space

Version 0.8, 19 October 2026. This document specifies the new default ecology and takes precedence over the v0.7 ecology in MATHEMATICS.md. The older ecology remains available only through `World(systems=False)` for regression experiments.

## The role interpretation

The **protector is the environment boundary**: it creates and maintains the conditions in which the healer and children can exist. It is not the Y spatial axis. Energy, material and information are quantities/representations that can exist in every role; they are not exclusive identities assigned to one role.

The **healer is the food-producing process and the timed food it manifests**. The producer needs a safe space and its own reserve. Each food has a birth tick, deadline and phenotype. Food's viability is its remaining availability; this prototype does not pretend a food particle has an independent planning mind.

The **children are snakes A and B**. They seek their own viability, compete for a shared food pool, observe each other and return contributions to the other roles.

Every role contains bounded models of every other role. Each role combines functions often associated with the others: the protector observes and repairs; the healer consumes substrate and transforms it; children maintain a body boundary, sense, act and contribute. The role names identify primary purposes, not mutually exclusive abilities.

## Reciprocal relationships implemented

| Provider → receiver | Executable contribution |
|---|---|
| Protector → healer | Boundary integrity and its model gate safe production |
| Protector → children | The bounded world and shared collision rules preserve a viable space; complete failure ends child activity |
| Healer → children | Regular/enriched timed food supplies energy and structural growth |
| Healer → protector | Uneaten food at its deadline supplies reserve for upkeep and repair |
| Children → healer | Each non-toxic food consumption transfers up to 2 battery GU to the healer; this is recorded as pollination |
| Children → protector | Up to 1 battery GU per non-toxic consumption is contributed when that child's protector estimate is below 85 |
| Children → information field | Movement writes signal trails; queued observations also write signals |

These are deliberately designed game relationships. “Pollination” names an abstract energy contribution, not a claim that these snakes implement biological pollination. Signal trails are available for inspection; the protector does not yet localize damage from them.

## Protector state and uncertain influence

Six faces carry integrity h_f∈[0,100]; H=min_f h_f is the conservative boundary indicator. Initially all faces are 100; protector reserve P=120 GU. Each tick selects one face with a separate seeded random generator and draws damage uniformly from integers 0,…,3+u, where u∈[0,10] is external pressure. This is a bounded uncertainty envelope, not an identified external attacker or a measured probability distribution. The seed makes experiments reproducible without claiming uncertainty has been eliminated.

User-mapped stress increases u, capped at 10. Every tenth tick u decreases by one. Support reduces u and adds 8×intensity GU to P as explicit external energy. Information increments a novelty budget. All causes, mapped inputs, locations and application ticks are inspectable.

At the start of a tick, expired food is consumed by the protector. A regular/enriched food adds 12/18 external GU to P. A toxic food instead spends up to 6 reserve GU in detoxification and damages the weakest face by 2. Consumed food material moves to the compost ledger. It is unavailable to either child in that same tick: deadlines take precedence over movement.

At tick end upkeep spends up to 1 GU. The weakest face is repaired by up to 3 points, each costing one reserve GU; when the protector's child-viability estimates include a value below 30, its repair budget rises to 4. Repairs cannot exceed 100. GU spent becomes system heat. Integrity is a separate structural variable, not an energy amount.

Crossing H=0 latches protector failure and deactivates all children. A failed boundary does not repair or restart itself; reset starts a new experiment. Its state remains inspectable.

## Healer safety, production and food viability

Healer vitality V starts at 100 and reserve R_h at 80 GU. Production is safe only when the boundary has not failed, actual H≥40, the healer's protector estimate≥40, and **every child** is alive with at least 8 battery GU. This literal rule encodes the stated dependence on both child and protector safety. Losing one child can therefore stop new production even though the other still moves. The healer can recover from a temporary unsafe period if safe conditions return before the ecosystem becomes inactive.

A safe tick adds one vitality point to a maximum of 100 and 3 externally supplied reserve GU. An unsafe tick loses two vitality points to a minimum of zero. Upkeep spends up to 1 GU. If safe, V≥20, reserve≥1 and food count<80, one vacant cell receives food at a cost of 1 reserve GU. The spawn excludes all body cells and special resources. There is no production if no cell is vacant. Food material supply is recorded explicitly; reserve spent becomes heat.

Food phenotype and lifetime:

| Food | Lifetime from birth | Child outcome | Protector outcome at expiry |
|---|---|---|---|
| Regular | 45 ticks | 12 + digestion GU; growth | +12 reserve GU |
| Enriched | 30 ticks | 18 + digestion GU; growth | +18 reserve GU |
| Toxic | 20 ticks | Up to 18 battery GU lost to heat; material still becomes one body segment | Detoxification cost and structural damage |

Initial regular food is staggered to expire at ticks 25+(cell index mod 55). New information consumes one novelty unit per new food: pressure≥5 or H<65 yields toxic food; otherwise H≥85 yields enriched food; otherwise regular. Without novelty, pressure≥5 creates toxic food on every third tick; when not in that branch, H≥90 creates enriched food every seventh tick; otherwise regular. These thresholds are configurable design assumptions, not discovered natural laws.

Automatic snakes exclude toxic food cells even as transit paths, and do not target food whose deadline will be reached before their estimated arrival. At decision tick n, a route of d cells arrives at n+d−1, since its first move happens in the current tick; food is eligible only when expiry>n+d−1. Enriched food adds six units to their route value. Reciprocation is paid from child battery after non-toxic intake. Toxic food is undesirable even though its material can grow a body; manual steering can expose that tradeoff.

The seven v0.7 special-resource types remain explicit effect tokens. Their renewal is gated by H≥40 and positive healer vitality; existing tokens keep their own expiry. They are not silently counted as physical food material.

## Shared ledgers and transition order

Let E be the shared energy field, Q_a child batteries, W_a child heat, P protector reserve, R_h healer reserve, W_s system heat, J cumulative external GU supplied. In the default two-child world:

ΣE + Σ_a(Q_a+W_a) + P + R_h + W_s = **20,320 + J**.

The initial 200 additional GU is the two system-role reserves. Food energy is recognized as external chemical energy **at intake**, rather than stored GU attached to food sites. The representation is explicit accounting for an open system, not a closed physical biochemical model. Reserve contributions transfer internally; upkeep, repair and detoxification transfer reserve to heat. Support and healer substrate enter J. Spatial background energy input remains explicitly supplied as before.

If M is live food material, B_a bodies, C compost and G supplied food units:

ΣM + Σ_a|B_a| + C = **86 + G**.

Expired food moves one material unit to compost; ordinary consumption moves it to body; body shedding moves it to compost. Compost is retained, not yet automatically turned back into food.

One live world tick: validate/log action → increment tick and expire buffs → apply queued mapped observations → draw uncertain boundary damage → protector consumes expired food → latch boundary failure if needed → both children sense/plan → simultaneous collision resolution → diffuse energy and decay signals → move, consume and reciprocate → child metabolism → spatial energy input → protector upkeep/repair → healer safety, upkeep and production → special-resource expiry/renewal → update bounded models → output snapshot.

Input signal writes precede the signal decay in that tick. All-dead worlds remain frozen; queued observations require a live tick to apply. Use reset for another experiment after complete collapse.

## Models containing models

Roles r∈{protector,healer,child_A,child_B} observe normalized viability truth z_r. Protector truth is H; healer truth V; child truth is floor(100×battery/capacity), clamped to [0,100] and zero if inactive.

For each ordered pair (a,b), update μ_ab←floor((μ_ab+z_b)/2). Store the previous b→c estimates as second-level scalars ν_abc. This has 16 first-level entries and 64 scalar submodels, not cyclic/infinite recursion. Timestamps show observation phase. The healer uses its protector estimate in production; the protector uses child estimates in repair allocation; children use their protector estimates for contributions. The existing snake-to-snake position/prediction models still govern competition. Some other entries remain diagnostic summaries; no general cognition or optimal inference is claimed.

## Input → encoding → matrix → output → interpretation

1. **Define a system boundary and role mapping.** A real domain must supply entities, units, relationships, observation rules and what counts as viability.
2. **Observe and choose meaning.** A human selects stress, support or information and gives the observation a provenance label. This semantic classification is a modeling choice.
3. **Normalize/quantize.** Supply an integer 0–10 using a documented domain scale. This implementation validates that scale; it does not invent a conversion from arbitrary raw units. Keep the original measurement outside the simulation if its precision matters.
4. **Locate.** Supply a 0–9 coordinate triple, or map label deterministically by the first four bytes of SHA-256(label) modulo 1000 and invert x+10y+100z. Collisions are possible. Locations are representational addresses, not an automatic physical embedding.
5. **Encode and queue.** `/api/input` accepts an expected tick and typed input. Up to 64 events are queued. Their bounded signal and pressure/support/novelty effects apply on the next live tick. Accepted inputs are included in replay history; labels are data, never executable instructions.
6. **Compute.** The same authoritative Python transition updates interacting roles, resources and children.
7. **Decode.** `/api/output` exports role viability, child outcomes, protector consumption, mapped input provenance, uncertainty wording and a next-question prompt. The desktop interface displays the same outcomes and underlying models; desktop and VR show the same world.
8. **Interpret and iterate.** Compare runs, question the role assignment and thresholds, formulate another input, and repeat. The output is simulation evidence under these rules, not a validated forecast about an arbitrary source system.

Example input:

```json
{"tick":0,"input":{"label":"Unknown boundary disturbance","kind":"stress","value":4,"position":[2,3,4]}}
```

The project is now a runnable **framework scaffold** for systems experiments. Applying it to another domain still requires explicit adapters, domain calibration, conservation/constraint choices and validation against observations. A finite 1,000-cell matrix does not by itself make every possible system representable without information loss.

## Presentation and limits

The role panel displays protector, healer and children viability, reserves, six face integrities, current uncertainty and contributions. The cube outline changes from green toward red as integrity falls. Food cells expose phenotype and remaining ticks; enriched food is light green, toxic food red. The input form queues experimental observations, and the output can be inspected/exported. The separate folding lab remains a mathematical demonstration, not an automatic generator of physical boundary topology.

These are engineered causal interactions and bounded adaptation. No assertion of consciousness, universal inference, unlimited growth, guaranteed viability or general-purpose prediction is made. Physical headset features remain untested.

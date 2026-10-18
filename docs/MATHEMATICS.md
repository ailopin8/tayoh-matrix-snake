# TAYOH Matrix Snake — core mathematics through v0.7

**v0.8 default ecology:** see [SYSTEMS_FRAMEWORK.md](SYSTEMS_FRAMEWORK.md). It supersedes the food-renewal, role-identity, input/output and ledger rules below. The earlier ecology is retained with `World(systems=False)` for focused regression tests; the default now includes protector and healer reserves, timed food, reciprocal role models and uncertain damage. Spatial indexing, collision resolution, diffusion and finite snake-to-snake modeling remain in use.

## State and interpretation

A proposed game system, not a physical theory. V={0,…,9}³; i(x,y,z)=x+10y+100z. Edges connect axis-aligned neighbors. No wrapping; diffusion has no-flux walls and the snake collides at exterior faces. X=Energy, Y=Material, Z=Information are spatial identities, not quantities.

Two snakes A and B share all fields and resource sites. Each has its own body, battery, heat, score, timed buffs, visits, purpose models and opponent model. A starts green at [(4,4,4),(3,4,4),(2,4,4)] facing +X; B starts blue at [(5,6,5),(6,6,5),(7,6,5)] facing −X. Each starts with 60 GU. Defaults below apply per snake unless identified as shared.

State includes integer energy E(v)≥0, binary food M(v), signal I(v)∈[0,30], ordered unique snake body B, battery Q, heat ledger H, score R, direction D, timed buffs, resource sites and expiry ticks, visit counts, resource-consumption counters, finite recursive purpose models K, cumulative supplied energy J, supplied food G, and compost C.

Initially E=20 at every site, Q=60, H=R=J=G=C=0; B=[(4,4,4),(3,4,4),(2,4,4)], D=+X. Seeded Python Random places 80 foods excluding both bodies and 14 special resources excluding food/both bodies. Catalog kinds cycle in fixed order; vacant positions use the seeded generator. Matching seed, code/runtime version and accepted actions determine replay. Save the world snapshot for cross-version archival: random sampling is not a universal cross-language contract.

## Transition order

A live world step validates names and boolean auto flag, logs the submitted action, increments tick n, and expires both snakes’ buffs with expiry≤n. Both sense the same pre-movement state and choose intents before either moves. Automatic mode ignores manual direction/skill intents and invokes the planner; B is always automatic while the checkbox controls A. Manual mode rejects immediate reversal. Manual shield/harvest/scan costs 12 GU transferred Q→H and lasts five ticks. Then:

1. Synchronous integer energy diffusion from old E.
2. Signal decay I(v)←max(0,I(v)−1).
3. Propose head h=B[0]+D. Food at h means growth; collision includes the tail only on growth. Both snakes’ complete opponent bodies, including opponent tails, are blocked. Automatic blocked moves yield in place and still pay metabolism; manual A collisions kill unless shield is active. Dead bodies remain structural obstacles. No phasing through walls/body occurs. If both valid intents claim the same vacant cell, the snake whose index equals n mod 2 advances; the other yields. Priority alternates by tick, regardless of iteration order or score. This is equal opportunity, not equal outcomes. Head swaps are blocked by body exclusion. All collision permissions are decided before either body is mutated; a yielded tail cannot accidentally be treated as vacant.
4. On movement, prepend head. Food is cleared and score increases; add 12+min(3,floor(R/20)) external GU to the battery subject to capacity. Every third food activates harvest for five ticks. Retain the tail for food, otherwise remove it. If body exceeds 24, remove one tail and increment compost.
5. Consume any special resource at h, increment its consumption record, apply its effects and remove the site. Record this tick's event and head visit.
6. Transfer g=min(E(h), harvest?8:4, max(0,capacity−Q)) from E(h) to Q. Write I(h)=30 for scan, otherwise 10.
7. Transfer metabolic cost min(Q,m) to H. Zero Q kills. Collision steps still have metabolism, diffusion and ecology.
8. Apply environmental energy supply, food renewal, special-resource expiry/renewal; update purpose models and snapshot.

A dead snake stops moving and metabolizing but its body and residual energy remain in the ledgers. The surviving snake continues; the world stops only when both are dead. Dead worlds do not advance, regenerate, or restart automatically. Effects acquired during tick n last through n+duration−1, including the current metabolic charge. Buffs with different names coexist; reacquiring the same name replaces its expiry (possibly shortening it). Automatic every-third-food harvest can therefore replace a catalyst's longer harvest duration. This explicit precedence can affect foraging outcomes.

## Resource catalog and context-dependent value

Food is primary: it grows structure, restores battery, and increases score. Seven special kinds coexist, with 14 sites maintained. Each site expires 100 ticks after creation unless consumed first. Renewed sites exclude body, food and other resources.

| Kind | Consumed effect | Automatic desirability U |
|---|---|---|
| Capacitor | Up to 30 battery GU from external supply; +2 metabolism for 8 ticks | min(30,capacity−Q)−16−2 floor(body length/8) |
| Shield crystal | Collision absorption for 10 ticks | 9 if shield absent or nearly expired (≤n+2), otherwise −1 |
| Harvest catalyst | Local extraction up to 8 GU for 12 ticks | 10 if snake's aggregate energy estimate≥4000 and harvest absent; otherwise −1 |
| Memory spore | Scan trail intensity 30 and +3 preference for unvisited target cells, 16 ticks | 5 if scan absent, otherwise −1 |
| Recycler enzyme | Shed up to three tail segments while retaining at least three; shed material→compost | min(12,max(0,body length−6)×2)−2 |
| Toxin | Immediate min(25,Q) GU loss to heat | −1000 |
| Overload seed | Up to 40 battery GU; +5 metabolism for 10 ticks | −1000, because added cost totals 50 GU |

These are transparent designed utilities, not learned beliefs or a proof of optimal control. The resource catalog is known to the snake; there are no hidden resource identities. Immediate battery changes and encounter counts are recorded for inspection, but those counters do not train a policy. Low-value resources are treated as avoidable cells in automatic routing; manual mode can consume them to test effects. Buff interactions are compositional: capacitor and overload costs add, harvest and food affect energy intake, recycler changes body geometry and metabolism, and scan changes target scoring and information traces.

## Autonomous instruction and algorithm

Instruction: keep seeking and consuming reachable food, favor safe routes, and accept optional resources only when their current designed utility is positive.

Each tick runs a breadth-first graph search from each head. Internal body cells and all opponent body cells are blocked. Immediate neighbors matching the opponent’s straight-line predicted head are also avoided. These predictions can be wrong; the collision resolver still prevents overlap. The departing tail can be traversed on the first move if it does not grow; treating its current position as available later in the path is an approximation. Immediate direction reversal is excluded at the first expansion. Resource cells with U≤0 are blocked. All food and resource positions are known: this is full-map sensing, not partial observation or hidden-state inference. BFS supplies shortest distance d and first move a for each reachable cell.

Food base value is 32+max(0,55−Q); optional resources use U. An active scan adds 3 for an unvisited target. For each living opponent, multiply the value by 0.65 when its Manhattan distance to the resource is less than the snake’s BFS route distance; multiply by 0.8 when the opponent’s previous target is this resource. This discourages contested chases without granting exclusive ownership. Rank by discounted value/(d+1), then shorter distance, then lower cell index. Before accepting a first move, flood-fill its predicted free volume after immediate growth/tail departure. Stop the count at |B|+6. Prefer a candidate only if the count is at least |B|+2. This is a bounded escape-space heuristic, not a proof of future survival.

If no such resource route exists, choose a legal first move maximizing free volume, then current local E, then fewer visits, then fixed direction order. If no legal neighbor remains, keep direction and report trapped. Shield may buy time but does not create an escape route. Replan every tick: future body geometry and new resources can invalidate a previous path. Finite-volume checks cannot rule out every trap or starvation scenario.

The recursive snake→energy estimate now causally influences catalyst utility. Other model summaries remain diagnostic; the controller is not a recursive belief optimizer. The policy neither purchases manual skills nor conceals a second simulation inside the renderer.

## Energy and material accounting

For each positive-coordinate undirected edge {i,j}:

f_ij=sign(E_i−E_j) floor(|E_i−E_j|/12), with f_ji=−f_ij.

E'_i=E_i−Σ_j f_ij. Flux is equal/opposite, hence ΣE is conserved by diffusion. At most six outgoing fluxes each≤E_i/12 preserve nonnegativity. Quantization intentionally leaves small gradients unchanged.

This version is an **open system**. Each tick, for j=0,…,9, select cell i=(37n+97j) mod 1000 and add min(4,max(0,40−E_i)) GU. The supplied amount enters J. Food battery gains and capacitor/overload supply also enter J. Battery capacity c=100+10 min(5,floor(R/20)). Any supplied energy above capacity becomes heat, not erased. Local extraction stops at capacity. Skills, toxins and metabolism transfer Q→H.

Therefore ΣE+Σ_a(Q_a+H_a)=20,120+J exactly for the two-snake world (20,060+J in explicit one-snake tests). Heat remains a bookkeeping sink, not a spatial temperature field. Food provides externally supplied chemical energy abstractly; material units and GU are distinct ledgers.

Metabolism m=2+floor((|B|−3)/8)+2·1_capacitor+5·1_overload. Replacing the old score-proportional unbounded cost prevents inevitable starvation solely from score growth.

When food count<80, create at most one food on a seeded random vacant site each tick and increment G. If no vacant site exists, supply is skipped. Food consumption converts a material unit into body length; bounded growth and recycler shed body units to C. Thus ΣM+Σ_a|B_a|+C=86+G in the two-snake world (83+G with one). Compost is retained in the ledger; it is not yet recycled back into food. Renewable food is external material supply, explicitly accounted for.

Special resources are abstract effect tokens, not food/material units. Their spawn/despawn is not governed by the material ledger. If they later become physical particles, their quantities must be added to the conservation model.

## Structural adaptation, time, and open-endedness

At each 20 foods, digestion increases by one GU per food to a maximum +3 and capacity rises by 10 to a maximum 150. Body length≤24, minimum 3, and shedding changes geometry, metabolic burden and escape space. These are explicit bounded developmental rules, not genetic evolution, reproduction, or open-ended learned intelligence. Different trajectories arise from resource timing, geometry, route decisions and interacting buffs; no specific emergent behavior is guaranteed.

There is no prescribed final score or tick limit. Renewable external inputs make continued operation possible, but do not guarantee infinite survival. The cube, active resources and adaptations are bounded; tick, score, heat, compost and action-history counters can grow without a designed cap. Very long runs consume growing history memory and may need streaming logs in a production version. “Infinite” here means no scripted end, not physically unlimited memory or a proof of an immortal snake.

Logical Δt=0.2s per live step. The client playback period is max(150,500−5R) ms. Wall-clock pacing changes, not F or Δt. A browser Run clock submits actions; Python is the sole authoritative state transition. Pausing/closing clients pauses the world. Expected tick numbers and a server lock serialize competing clients; use one Run clock for reproducible experiments. Auto mode is a local client checkbox (enabled by default), logged on every accepted action so replay reproduces decisions.

## Mutual sensing and competition

For ordered snake pair (a,b), O_ab(n) stores b’s head, body, direction, battery, score, alive status and previous target, sensed before movement at tick n. The timestamp identifies the decision phase; the stored head can differ from the post-movement head in that tick’s returned snapshot. The constant-direction prediction is p̂_b=h_b+D_b if in bounds and alive, otherwise h_b. It is a hypothesis, not knowledge of b’s newly computed intent. Information is full-map and public; no sensory radius, occlusion or learned inference is claimed.

Each O_ab additionally stores a shallow copy of the head/prediction/timestamp that b previously held about a. This bounded “my model of your model of me” is one-step delayed and never nests further. The first observation has no prior nested model. It exposes reciprocal representation without infinite recursive objects.

The body and predicted-head observations affect collision avoidance; observed head and last target affect resource scoring. Both choose independently, with the same rules and resource pool. Nothing forces them to split food equally, share energy or preserve the competitor. Yielding avoids immediate destruction; survival remains individually driven. Score, battery, body size, special-resource consumption and decisions are shown separately. There are no separate food copies or hidden bonuses for B.

## Finite recursive models

Each snake independently maintains P={energy,material,information,snake}; truth z_a=(ΣE,ΣM,ΣI,Q_a). For each ordered pair a,b, μ_ab is a scalar estimate plus tick and four second-level scalars ν_abc. Initialize μ_ab=z_b and ν_abc=z_c. Update synchronously:

μ_ab^(n+1)=floor((μ_ab^n+z_b^(n+1))/2), ν_abc^(n+1)=μ_bc^n.

Thus every purpose contains a model of every purpose, including their previous estimates. There are 16 first-level entries and 64 second-level scalars, no cyclic references or infinite recursion. Aggregate observations are shared, so estimates often coincide; they are not differentiated cognition. Floor averaging has downward rounding bias. I is a decaying visit signal, not Shannon information or a physical bit count. Scan changes both visible trail duration and controller scoring without implying that signal is literal energy.

## Boundary creation and compression

The source images show a central red set, surrounding blue points, a straight cut after a fold, and a closed polygon after unfolding. They motivate this illustration but do not supply enough crease, layer, topology or cut data to reconstruct the depicted physical construction.

Use continuous domain D=[0,9]² and explicit noninjective feature map

F(x,y)=(u,v)=(max(|x−4.5|,|y−4.5|),0).

For 0<r<4.5, half-space classifier u≤r pulls back to the closed square C_r=[4.5−r,4.5+r]². The vertical line L_r={u=r} has preimage ∂C_r, a closed piecewise linear separator in D. This is a preimage operation, not the forward image of a line under an inverse homeomorphism. F discards angle and collapses many points; there is no unique inverse. Original point IDs are retained to display unfolding; compressed coordinates alone cannot reconstruct the original state.

The demo samples all 100 integer grid sites; red means u≤2.5 (36 sites), blue means u>2.5 (64). Changing r reports true red and blue counts inside. Compression slider t draws G_t=(1−t)(x/2,y/9)+t(u,1/2) with display scaling; intermediate configurations are visual interpolation, not asserted physical crease motions. The square remains visible in the original panel and the vertical threshold in the compressed panel.

A general line under a nonrigid folding map does not necessarily yield a closed separator. An injective homeomorphism preserves topological type, so it cannot turn an interval into a circle. A noninjective map may have disconnected, open, branched or empty line preimages. Closure here follows only from the stated max-norm level set and radius range. A physical cutting construction additionally needs sheet topology, crease geometry, layer incidence, which layers are cut, and an unfolding correspondence. Separating finite labeled samples also does not prove separation of arbitrary continuous regions.

The boundary lab is a mathematical sandbox; it does not alter world collision boundaries. Coupling it to the world would require an explicit voxelization and collision rule and a revised material/energy ledger.

## Shared desktop / VR presentation

The 10×10 slice chooses any normal axis and depth 0–9. Cells expose exact coordinates, fields and resource identity; layer buttons reveal body counts. Green A and blue B appear in both the slice and shared cube. Layer counts include both bodies. Resource cards show effects, desirability and consumption counts for each snake. Decision text and meters report both snakes independently; expandable models expose mutual observations and finite purpose models. Desktop and WebXR meshes read the same Python snapshots.

Positions map to (p−4.5)/10 meters around a one-meter cube centered 1.3m high, 2m forward. VR changes cameras only. Enter VR requests immersive-vr from a click, requires support, permission and secure context, and attaches the session to Three.js. No headset HUD/hand tracking is implemented. Controller select cycles a manual direction intent for A; uncheck Autonomous A before using manual steering. B remains autonomous. Enable Run before entering VR. Hardware features remain unverified.

## Primary technical references

- W3C WebXR Device API: https://www.w3.org/TR/webxr/ — session lifecycle, secure context, tracking, user activation.
- Three.js WebXRManager: https://threejs.org/docs/pages/WebXRManager.html — renderer session attachment and reference spaces.
- Vendored Three.js 0.170.0: https://github.com/mrdoob/three.js/tree/r170 — MIT license included. The dependency is pinned; the project makes no claim this is the latest release.

The game equations above are original proposed rules, not attributed scientific results. The closed square preimage is derived explicitly above and can be checked directly.

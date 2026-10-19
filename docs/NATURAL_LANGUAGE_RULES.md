# Plain-language instructions — v0.14

An instruction states the intended change, names the affected component and maps to a bounded Python policy. The purpose of an input is expressed as a sentence; its numerical implementation and trade-offs are explained before confirmation. Spatial coordinates remain an internal representation and an optional advanced tool.

| Instruction | Mechanism |
| --- | --- |
| Help the boundary repair more damage | Repair budget 5 reserve units/tick, instead of normally 3 (4 when child estimates indicate distress). Faster reserve depletion is possible. |
| Help the boundary conserve its energy | Repair budget 1; slower repair may allow damage to accumulate. Maintenance still costs 1. |
| Make the food producer more cautious | Boundary and boundary-model estimates must be ≥65 instead of ≥40; production opportunities only every third tick. All other safety, capacity, reserve and occupancy checks remain. |
| Restore normal food production | Restore threshold 40 and production opportunity each tick. |
| Make the snakes give each other more space | Target desirability multipliers 0.35 when opponent is closer, 0.5 when opponent targets the same cell. Both discounts combine. |
| Make the snakes compete more strongly | Multipliers 0.9 and 1 respectively. Collision, toxicity, energy and path safety rules remain. |
| Restore the original rules | Default policies for all roles; no world reset or reserve replenishment. |

These are alternative decision policies, not just text labels or injections of free energy. Child policies affect both autonomous planners; manually steered A does not use the planner until autonomy is enabled. Policy changes never promise survival or a particular emergent outcome.

`instructions.interpret(text)` normalizes case, spaces and punctuation and matches registered sentences or keywords. Unsupported language is rejected with an explanation. This is a deterministic, limited vocabulary, not an LLM, arbitrary semantic understanding, or execution of user-provided Python. Additional algorithms require implementing and testing a recipe. Existing numerical support/stress/information inputs remain independent, one-time interventions.

`POST /api/interpret` returns a read-only preview. On confirmation, `/api/input` queues an instruction, records its canonical text in replay history, and changes no active policy yet. At the next logical tick `Systems.start()` interprets and applies queued policies in order before role decisions. A later instruction for the same role wins. Policies persist until changed or world reset. The processed log contains the recipe, effective tick and explanation; state exposes current policies and natural-language descriptions. Pending rules can affect an in-flight live run on a following tick; pause before reviewing if exact tick timing matters.

The desktop selector presents full sentences, with optional typed supported phrases. VR's Try rule previews repair for the boundary, caution for the producer, or cooperation for either selected snake. Apply rule confirms the pending draft; Cancel draft discards it. These ray controls retain the explicit review stage and show the rule effect in the component card. Larger rule choices remain available in the headset's normal browser interface before entering VR. Quest hardware interaction remains untested locally.

Verification includes recipe parsing, unknown-input atomicity, next-tick activation, restoration, actual repair/production/target changes, deterministic replay and energy/material conservation. The same Python is shipped into the browser worker and used by the local server. Detailed source: instructions.py, systems.py and engine.py.

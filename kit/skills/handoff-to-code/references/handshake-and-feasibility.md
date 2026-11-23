# Handshake, not handoff, and feasibility first

Read this file at steps 2, 3 and 18 of `handoff-to-code`. It covers how design and build run in parallel with sync points, who owns what, and how to prove risky parts with a spike before any high-fidelity work.

Evidence. The handshake model, the fidelity ladder, the spike rule and the real-data rule come from the Design Engineering Handbook (DesignBetter), chapter 2, read through the GDH research: DOCUMENTED as method. The sync point defaults are this kit's own: UNTESTED until a project uses them.

Terms. A handoff is a sequential transfer: design finishes, then the build starts. A handshake is parallel work with repeated sync points. A spike is a small working build that answers one feasibility question. A sync point is a dated meeting of design and build state.

## 1. Why a handshake

A single transfer point hides the edge cases that only appear while building. By then a change is expensive. Parallel work shows them while a change is still cheap. The design package is still written, but it is a living contract, updated at each sync point.

## 2. The sync points

| Sync point | When | Design shows | Build shows | Output |
| --- | --- | --- | --- | --- |
| Kickoff | Before high fidelity | Brief, chosen direction, scope list | Stack, component library, data shape, risk list | Ownership table; spike list |
| Spike review | After each spike | The design intent the spike tests | The working spike | Feasible, feasible with change, or not feasible |
| First screen | The first built screen renders | The package for that screen | Captures at each breakpoint | QA findings; edge cases found |
| Mid-build | About halfway, or per milestone | Updates from edge cases | Built screens | A dated package section |
| Release | Before launch | Final package | Full captures, check results | Design QA pass; handoff closed |

Default: a sync point at direction, at the first built screen and before release. Add the spike review and mid-build points when the risk list is long.

Rules:

1. Each sync point ends with a dated entry in `design/decisions.md`: what changed, who decided.
2. Edge cases the builder found go into the next package section, not into chat only.
3. Locked items grow at each sync point. A change to a locked item asks "reopen?" with its cost.
4. A same-session build with one agent needs short notes, not a long spec. Spec length grows with distance between design and build.

## 3. Ownership

Write this table into section 2 of `design/handoff.md` at kickoff.

| Item | Design side owns | Build side owns |
| --- | --- | --- |
| Brief, direction, decision record | yes | reads |
| Tokens and `DESIGN.md` | values and names | how tokens enter the build |
| Component inventory: props, variants, states | what each must show | the API shape and the code |
| Layout and breakpoints | the rule at each width | the CSS that implements it |
| Motion | intent, tokens, reduced-motion behavior | the implementation and its performance |
| Copy and content | every string | string storage and localization plumbing |
| Assets and licenses | the choice and the record | loading and optimization |
| Data, routing, storage, auth | the visible states they cause | everything else |
| Acceptance checks | the pass conditions | running them and fixing failures |
| Design QA | the review of the render | the captures |

Neither side edits the other's files without asking. A builder that needs a new token asks for one. A designer that wants a code change writes it as a finding.

## 4. Feasibility before high fidelity

High fidelity on an idea that cannot be built wastes both sides. List risky parts at kickoff and spike them.

Risk signals:

| Signal | Example | Spike question |
| --- | --- | --- |
| Novel interaction | Drag to reorder across lists | Does it track input and stay interruptible on the target devices? |
| Heavy motion | Shared-element route transitions | Does it hold frame rate on a mid-range phone? |
| 3D or WebGL | A rotating product model | Does it load inside the size budget and fall back when WebGL is lost? |
| Live data | A chart over streaming values | Does the chart read with real, flat, empty and extreme data? |
| Unknown fields | A form for a backend not yet built | Which fields exist, which are required, what errors return? |
| Third-party embed | A map or a video player | Can it take the tokens and the focus rules? |
| AI feature | An answer box over a model | Which states occur: fast, slow, limited, failed? |

Procedure:

1. Write a spike statement: "This spike tests whether <part> can <behavior> on <device or stack>."
2. The build side builds the smallest version. Prototype code is labelled prototype and never merged as production.
3. Run it with realistic data: real or realistic values, including a flat, an empty and an extreme case.
4. Record the result: feasible, feasible with change (say the change), or not feasible.
5. Not feasible: return the part to the discipline skill with the constraint. Offer at least one alternative.
6. Raise fidelity only after the spike answered its question.

Fidelity ladder:

| Confidence | Fidelity | What it settles |
| --- | --- | --- |
| Low, many options | Sketch or rough board | The idea |
| Narrowing | Low-fidelity wireframe, content types labelled | Structure and flow |
| Structure agreed | High-fidelity static with real content | Content, hierarchy, look |
| Look agreed | Interactive prototype with mock data | Interaction, edge cases, motion |
| Interaction agreed | Prototype with real data, or the build | Behavior with real values |

Move up one step only when the current step's question is answered.

## 5. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Throw over the wall | One transfer, then silence until launch | Set sync points at kickoff |
| Pixel-perfect fantasy | High-fidelity screens for a part nobody tested | Spike first; lower the fidelity |
| Nice-data chart | The chart was only seen with invented smooth data | Spike with real, flat, empty and extreme data |
| Silent cut | A state is dropped for time and nobody decided | Record it as a simplification with a name |
| Spec drift | Mockup and spec disagree | One reference file per screen; the package names which one is the truth |
| Flat "no" | A request rejected on feasibility with no option | State the constraint and offer an alternative |

## 6. Worked example

Scope: a booking app's calendar screen. Risks at kickoff: drag to move a booking; a week view on a 320 px phone.

1. Spike 1: "This spike tests whether a booking can be dragged between days on iOS Safari and stay interruptible." Result: feasible with change. Long-press to start, because a plain drag fights scroll.
2. Spike 2: "This spike tests whether a week view reads at 320 px." Result: not feasible with seven columns. Alternative: a three-day view with a day picker. The owner accepts.
3. The design moves to high fidelity with both changes. The decision record gets two entries.
4. First-screen sync: the builder found that bookings can overlap. The design adds an overlap state in a dated package section.

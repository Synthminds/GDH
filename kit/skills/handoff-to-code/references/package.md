# The handoff package

Read this file at steps 7, 11, 13 and 14 of `handoff-to-code`. It covers the file set, the checks to run first, how each section of `design/handoff.md` is filled, the runtime sheet for AI features, and the failure patterns.

Evidence. The commands in section 2 were run on 2026-11-23 against a scratch project built from this kit's example brand pack: VERIFIED for the scripts and their exit codes. The package shape is this kit's proposal; no coding agent has built from one yet. Label a first use UNTESTED.

Terms. The package is the set of files a builder receives. The contract is `design/handoff.md`. A reference file is the one artifact that shows the truth for a screen.

## 1. The file set

| File | Holds | Made by |
| --- | --- | --- |
| `DESIGN.md` | The design system in prose with YAML front matter | `ds.py design-md` from tokens plus the brand book |
| `design/tokens.json` | Token values in the Claude Design System shape | `design-system` |
| `design/tokens.css` | Custom properties | `ds.py export` |
| `design/handoff.md` | The contract: scope, decisions, components, layout, motion, content, assets, checks, questions | this skill |
| `design/assets/manifest.json` | Source, license, attribution, date, path and hash of every outside asset | `find-assets`, `generate-media` |
| `design/decisions.md` | Dated rounds, choices and rejected options | every skill |
| `design/directions/<n>-<name>/` | Reference files: artboard exports, local HTML | discipline skills |
| `design/reviews/<date>-handoff-checks.md` | Output of the checks below | this skill |

Nothing else is the contract. A screenshot is never the contract.

## 2. The checks to run first

`DS` is the script of the `design-system` skill. `A` is the script of the `find-assets` skill. `T` is the script of the `design-critique` skill. All three run offline.

```
DS="python3 <design-system skill folder>/scripts/ds.py"
A="python3 <find-assets skill folder>/scripts/assets.py"
T="python3 <design-critique skill folder>/scripts/tells.py"

$DS validate  design/tokens.json
$DS contrast  design/tokens.json
$DS export    design/tokens.json --css design/tokens.css
$DS design-md design/tokens.json --readme <brand book README.md> -o DESIGN.md
$DS audit     design/directions --tokens design/tokens.json
$A  check     design/assets/manifest.json --root .
$T  design/directions --tokens design/tokens.json --design DESIGN.md
```

1. Each command exits 0 on a pass and 1 on findings. `audit` exits 1 while raw literals remain.
2. Save the output in `design/reviews/<date>-handoff-checks.md`.
3. A failing validation or a failing asset check stops the handoff.
4. A failing contrast pair goes to `color`. It stays an open blocker until fixed or accepted as a recorded exception.
5. Send raw values from the audit back to the discipline skill. Or list them in the handoff as "to tokenize", with an owner.
6. `design-md` rewrites `DESIGN.md`. When a person wrote prose in it, pass the brand book with `--readme`, or merge by hand. Ask before you overwrite.
7. A tell from the scan that the design system requires is brand-required, not a finding.

## 3. `design/handoff.md`, section by section

The template is the project file `design/handoff.md`. Keep its ten sections in their order. Add numbered subsections where this file says so.

| Section | Holds | Read |
| --- | --- | --- |
| 1. What to build | Scope paragraph, ranked list, out of scope | below |
| 2. Source files | Status of each file, ownership table | [handshake-and-feasibility.md](handshake-and-feasibility.md) |
| 3. Decisions the build must keep | Decision, reason, record, brand-required | below |
| 4. Screens, states and breakpoints | 4.1 Components, 4.2 Screen state matrix, 4.3 Layout and breakpoints, 4.4 Content and the copy deck, 4.5 AI runtime sheet | [components-and-states.md](components-and-states.md), [layout-and-motion.md](layout-and-motion.md), [content-and-assets.md](content-and-assets.md) |
| 5. Motion | The motion spec rows and the removed list | [layout-and-motion.md](layout-and-motion.md) |
| 6. Assets | Manifest ids, format, size, use, license line | [content-and-assets.md](content-and-assets.md) |
| 7. Acceptance checks | Check, pass condition, how to run | [acceptance-checks.md](acceptance-checks.md) |
| 8. Simplifications | What was cut, what the user loses, who accepted | below |
| 9. Open questions | Question, who answers, what it blocks | below |
| 10. Evidence | VERIFIED, DOCUMENTED, UNTESTED | below |

### Section 1: what to build, and what not

- One paragraph of scope: who uses it and the primary job, from the brief.
- A ranked list of screens, components or assets. Rank 1 is built first.
- An "Out of scope" list. Name what a builder might reasonably add and must not: a dark theme, a tablet layout, a settings page, animation on scroll.

Out of scope stops guessing. A builder who sees "dark theme: out of scope" does not invent one.

### Section 2: source files

Fill the status column for each file: `current`, `stale` or `absent`. Fix a stale file before the handoff. Add the ownership table from the handshake reference.

### Section 3: decisions the build must keep

| Decision | Reason | Record | Brand-required |
| --- | --- | --- | --- |
| One primary action in each view | The brief's primary job is one go or no-go choice | 2026-11-20 round 2 | no |
| The accent color only for the action and for alerts | Brand rule: one accent | DESIGN.md, Colors | yes |
| No carousel on the home page | Rejected in round 1: hides offers 2 to 5 | 2026-11-18 round 1 | no |

- Give the reason, not only the value. A builder who knows the reason can solve a case the design did not foresee.
- Mark a brand-required choice, so a later tell scan reports it as brand-required.
- List the rejected options a builder might reach for, with the reason.

### Section 8: simplifications

| Simplification | What the user loses | Accepted by | Date |
| --- | --- | --- | --- |
| Week view replaced by a three-day view below 600 px | Seeing a full week on a phone | the owner | 2026-11-21 |

A simplification that nobody accepted is an open question.

### Section 9: open questions

| Question | Who can answer | Blocks |
| --- | --- | --- |
| Can two bookings overlap? | Product owner | Calendar overlap state; check 6 |

Say what each question blocks. A builder may start on what is not blocked.

### Section 10: evidence

```
VERIFIED: token validation, contrast, audit and asset checks, run on <date>
DOCUMENTED: states, layout and motion, as designed in the reference files
UNTESTED: the built render, performance, a screen reader pass, real data volume
```

## 4. Front matter

```
---
status: active
updated: YYYY-MM-DD
scope: <one line>
target: <gch | other agent | team>
---
```

`status: template` means not filled. `status: active` means the builder may rely on it. On a replacement, set `status: superseded` on the old file and link the new one. A later change adds a dated subsection under the section it changes.

## 5. Subsection 4.5: the AI runtime sheet

Fill subsection 4.5, "AI runtime sheet", when the design includes a model-driven feature. Otherwise write "Not in scope." there. The design owns states and words. The code owns storage, thresholds and enforcement.

| Area | In scope | Design decision | Code decision | Stage |
| --- | --- | --- | --- | --- |
| Memory | yes or no | What the user is told is remembered; where to see, edit and clear it | Storage, lifetime | prototype or production |
| Retrieval | | Whether and how sources show beside an answer | Sources, ranking, context cap | |
| Cache | | What "updated" means on screen; which answers are never reused | What is cached, the threshold | |
| Routing | | Whether the route (model or tool) is shown | Which service handles which request | |
| Limits | | The copy at a limit: what happened, when it resets, what to do | The numbers, per user and per endpoint | |
| Monitoring | | A usage view if a dashboard is in scope | Metrics and alerts | production |

Each AI entry point needs five states: waiting, answered fast, answered slow, limited, failed or fell back. The fast path must not flash a loader. A value the code chooses later, such as a limit number, returns to the design as a copy change.

Vendor performance numbers in source material are claims, not facts. Do not repeat them in the package.

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Values without reasons | A list of hex codes and sizes | Name tokens; give the reason for each decision |
| Happy path only | One state for each screen | Use the state matrix; mark "not designed" |
| Screenshot handoff | The builder gets pictures | Reference files with real markup and tokens |
| Stale tokens | `tokens.css` differs from `tokens.json` | Regenerate at step 7 |
| Unrecorded assets | Files with no manifest record | Run the asset check |
| Silent simplification | A state is dropped and nobody decided | Section 8, with a name |
| Pending passed as final | No decision entry for the scope | Step 4; ask |
| Scope creep by the builder | A dark theme nobody asked for | Out-of-scope list in section 1 |

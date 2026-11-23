# GDH principles

This file explains how the kit is built and how its rules were decided. Read it before you write or change a skill.
The always-on rules are in [KERNEL.md](KERNEL.md). This file is reference text and loads on demand.

## 1. Precedence

Four sources can decide a design choice. The higher source wins.

| Rank | Source | Where it lives | Example |
| --- | --- | --- | --- |
| 1 | The user | The request, and the answers in `design/decisions.md` | "Keep the serif headline." |
| 2 | The project design system | `DESIGN.md`, `design/tokens.json`, a brand pack, a hosted design system | A violet gradient token |
| 3 | The brief | `design/brief.md` | "Calm, not playful" |
| 4 | GDH defaults | Skill text that starts with "Default:", and the tell scan | Three directions |

Rules of use:

- A lower source fills gaps. It never overrides a higher source.
- When two sources at one rank disagree, stop and ask the user. Record the answer in `design/decisions.md`.
- A gate is not a preference. The accessibility floor, the spend gate, the exposure gate and the license rule stay in force at every rank. When a higher source conflicts with a gate, say so and ask. Do not waive the gate in silence.
- A later user instruction replaces an earlier one. Log the change.

## 2. Brand-required choices are not tells

A tell is a visual habit that marks work as generic AI output. The tell scan is a rank 4 default.

- Run the tell scan only on choices that no higher source prescribes.
- When the user, the design system or the brief requires a listed habit, report it as `brand-required`. It is not a finding. It does not lower a score.
- Name the source in the report. Example: `brand-required: gradient headline (DESIGN.md, Colors)`.
- A brand-required choice still passes the gates. A required palette that fails contrast is an accessibility finding, not a tell.

## 3. The shape of a skill

One folder for each skill. The folder name equals the `name` field.

Frontmatter: `name` (kebab-case, 64 characters at most), `description` (third person; what it does and when to use it; 1 to 1024 characters), and `disable-model-invocation: true` for a user-invoked skill.

`SKILL.md` is a router. It holds 150 lines and 1,500 words at most. Its sections, in order:

1. Purpose and boundary: what the skill does, what it does not do, and which skill does that.
2. `## Before you start`: inputs, project files to read, and the precedence line.
3. `## Procedure`: numbered steps. "ASK:" marks a user decision. "GATE:" marks a spend or exposure point. "STOP:" marks any other blocking precondition, such as a closed interview, consent or the right to study. Each STOP line also appears in the gate list under Checks.
4. `## Tools`: the capabilities in use and how to pick a tool.
5. `## Checks`: gates first, then defaults.
6. `## Output`: files written and the closing report.
7. `## References`: a link to each file in the folder, with when to read it.
8. `## Sources`: a short list.

Other rules of form:

- Depth goes in `references/*.md`, 400 lines at most for each file.
- A skill reaches another skill by name, never by file path. One exception: a user-invoked GDH skill is loaded by reading `SKILL.md` in the sibling folder of that name, because the host cannot start such a skill for the model. The kernel's skill handoff line states this route for every skill; `ask-gdh` step 9 is its full form. `check` code `GDH_ROUTE_USER_SKILL` guards it.
- A skill routes by capability. It names a tool only as an example and links the tool card.
- A skill holds no price, credit amount, model id or tool count. The agent reads these live.
- Each skill folder holds a `refinement-log.md` with one line for each change: `YYYY-MM-DD | observation | change | files`.
- Six skills are model-invoked: `align`, `ask-gdh`, `design-brief`, `mood-board`, `find-assets`, `design-critique`. All others are user-invoked. The user types their command, or `ask-gdh` loads their `SKILL.md` and follows it.

## 4. Evidence labels

Every claim about a tool, a number or a result carries one label.

| Label | Meaning | You may write |
| --- | --- | --- |
| VERIFIED | Someone exercised it and saw the result. The note says what was exercised and when. | "The export produced a 1080p file." |
| DOCUMENTED | A primary source states it. Nobody exercised it here. | "The vendor guide states a daily limit." |
| UNTESTED | It comes from memory, a secondary page or a rule of thumb. | "Default: target 30,000 to 50,000 triangles." |

Rules:

- Raise a label only after a real call or a real render. Reading more text does not make a claim VERIFIED.
- A design report says what was checked and what was not. "Contrast: VERIFIED on 14 pairs. Screen reader: UNTESTED."
- When research marks a fact as unverified, from memory or a rule of thumb, write it as a default.

## 5. Gate versus default

A gate is a check that blocks delivery. A default is a starting value.

| | Gate | Default |
| --- | --- | --- |
| Written as | A plain rule in a `## Checks` gate list | A line that starts with "Default:" |
| Evidence needed | A verified number or a rule with no number | Any label |
| Who can change it | Nobody in silence. The user can accept a recorded exception. | The user, the design system or the brief |
| On failure | Stop. Fix it or get a recorded exception. | Note it and continue |

Known limit: the contrast ratios in kernel rule 12 are the WCAG 2.2 AA values. Their label here is DOCUMENTED. The research did not open the standard in this build. Read the standard before you cite a success-criterion number.

Gates with no number need no source: brief exists, direction chosen, license read, quote shown, record written.

## 6. How conflicts between sources were resolved

The research found sources that disagree. Each row states the decision that the skills apply.

| # | Topic | Resolution |
| --- | --- | --- |
| 1 | Tell lists versus a brand that uses the listed habits | Precedence decides. Scan only what the design system leaves open. Report a required habit as `brand-required`. |
| 2 | Verify the render, or do not | Split by output. An artifact type follows its own check rule. A code deliverable needs rendered verification as a gate. |
| 3 | Duration of interaction feedback | Default: 200 ms for direct feedback. Larger surfaces use the element table in `ui-motion`. |
| 4 | Brand motion tokens versus short UI motion | Brand tokens win for page-level and brand moments. The short rule applies to controls. Map each token to a role: control, surface, page, flourish. |
| 5 | Springs | The design system decides. With no system, use a spring only for gesture-driven or interruptible motion. |
| 6 | Shortest duration that reads | Default: 100 ms for motion that carries meaning. Shorter values serve press feedback only. |
| 7 | Feedback timing | GDH teaches three tiers: instant, short wait, long wait. When GCH is loaded, its single number governs. |
| 8 | Target size | Default: 24 px for pointer, 44 px for touch, 48 dp on Android. The stricter single GCH number stays valid. |
| 9 | Line length | Default: 45 to 75 characters for body text. |
| 10 | Contrast method | Gate on the ratio method. Report a perceptual-contrast score as advice only. |
| 11 | Large-text threshold | Use the standard's definition: 24 px, or about 18.66 px when bold. |
| 12 | Smallest type size | No single number. Each medium has its own floor, in one table in `typography`. |
| 13 | Number of directions | Default three. Two when brand rules are strict. Four at most. |
| 14 | How directions differ | It depends on the stage. Explore: options differ in idea. Refine: options differ in one named attribute. Each round names its stage. |
| 15 | Where rationale goes | An artifact follows its type rule. The rationale also goes in `design/decisions.md`, always. |
| 16 | Eyebrow labels | Row 1 decides. The user and the design system beat the ban. |
| 17 | Pure black versus tinted near-black | Do not hard-code either. Decide from the design system, then the brief. |
| 18 | Style catalogs by category | Brief first. Use a category catalog as a list of looks to move away from. |
| 19 | Items at one decision point | Default: four. A dashboard may show five to nine metrics as its ceiling. |
| 20 | Triangle budget for web 3D | Default: 30,000 to 50,000 for a hero model, 100,000 in view as the ceiling. Measure on the device. |
| 21 | First tool for a mood board | Order: a design canvas artifact when artifacts are available; a local HTML board otherwise; a shared editable board only on request. Component and asset libraries are reference sources, not board builders. |
| 22 | First tool for motion video | Route by need. Code-owned or brand-exact video: a local HTML video composer. Generated footage: a video generator. Scene work with templates: a scene engine. A shared hosted project: the hosted composer. Label UNTESTED until exercised. |
| 23 | Route to a vector logo | Concept: a vector-capable generator. Clean-up: redraw or vectorize, then check the paths by hand. Never deliver a raster logo. |
| 24 | A vendor website flow that bans other design rules | Use that vendor for assets by default. Use its site builder only when the user chooses it. Then its flow leads. |
| 25 | Size of the GCH description total | Unresolved. Both counts are near the GCH limit. GDH keeps its own budget small. |
| 26 | A tool that states two daily limits | Unresolved in the tool's own text. Assume the lower limit. |
| 27 | Artifacts in regulated organizations | Sources disagree. Ask the owner. Assume neither answer. |
| 28 | The standalone design site after its closing date | Use the vendor Help Center wording. Plan for full closure. |
| 29 | Easing on exits | Default: ease-out for entering and for exits the person watches. Ease-in only for a short exit off screen while attention moves elsewhere. Source: `ui-motion`, timing and easing. |

When you meet a new conflict: apply precedence, pick the stricter rule for a gate, pick the brief's side for a default, and add a row here.

## 7. Provenance and honesty

- Kit text is original. A skill names its sources in a short list: title and chapter, or a URL. It quotes nothing at length.
- The kit copies no code and no prose from another harness. It may name a skill of that harness and say when to call it.
- Third-party skills are offered, not vendored. The user installs them.
- The repository is public. It holds no address, account id, balance, workspace id, private URL or client name.
- No tool was exercised with a spend call when this kit was built. Tool cards say what was exercised.
- A catalog entry carries `verifiedAt` and `evidence`. `gdh.py doctor` reports stale entries.

## 8. Session alignment

Every GDH session opens with `align`. Kernel rule 0 states it. The owner chose an interview at the start of each session, because a design agent that guesses the audience, the job or the taste wastes the rounds that follow.

Three skills share the opening. None repeats another.

| Skill | Owns | Does not |
| --- | --- | --- |
| `align` | The interview: the topic tree, the question bank, the depth by job size, tier one and tier two, the alignment entry | Write the brief file or route |
| `design-brief` | The brief: its format, the status line, the persona form, the fidelity ladder, the quality tests | Ask interview questions |
| `ask-gdh` | Routing: the pre-flight, the plan, the first skill | Route before `align` has closed in the session |

Two tiers:

- Tier one, the full interview, runs when no brief reads `Status: confirmed YYYY-MM-DD by <who>`, or when the user asks for it.
- Tier two, re-alignment, runs on a confirmed brief. It asks three questions and escalates only the topics an answer touches.

Depth follows the job size: asset, page, product or brand. A one-icon request is not a forty-question interview. The depth table in `align` marks each topic required, optional or skipped.

The user stays in charge. "Skip" or "you decide" records the agent's proposal as ASSUMED. The user may end the interview at any time; the ASSUMED lines stand, and the brief says it ended early. The kernel does not allow skipping `align` entirely, because the re-alignment tier costs three questions at most.

`align` runs its own interview loop by default. It hands the interview to `gch:grilling` only when the description of that skill in the session contains the words "caller contract". Then `align` supplies the topic tree, the question bank and the loop rules. Otherwise it says that the GCH skill does not yet honor the `align` contract, and runs its own loop.

The question bank tags each question Book, Adapted or Derived. Book means the source holds the question or method. Adapted means GDH built it from a source method or case. Derived means GDH wrote it with no source. The bank reuses no statistic from its sources.

## 9. Coexistence with GCH

GDH decides how a product looks. GCH decides how code is built, tested and reviewed.

- When the GCH kernel is loaded, GCH governs code work. Its `ux-laws` numbers hold for screens.
- GDH hands work to code through `handoff-to-code`. The package is `DESIGN.md`, `design/tokens.json`, `design/assets/manifest.json` and `design/handoff.md`.
- GDH calls GCH skills by name when they are installed. Each GDH skill states a fallback for a host with no GCH.

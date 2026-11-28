# Pre-flight

`align` has already read the project and closed. Reuse what its closing report states. Run these five checks before you classify a request. Each check reads. None writes, spends or publishes.
Budget: finish in ten tool calls or fewer. Report what you did not check as UNTESTED.

## 1. Find the design system

Search in this order. Stop at the first source that is filled. Still list the others that exist.

| Order | Look for | Counts as found when | Authority |
| --- | --- | --- | --- |
| 1 | `DESIGN.md` at the project root | It has prose rules and its front matter does not read `status: template` | Rules |
| 2 | `design/tokens.json` | It parses and holds at least color and type families | Values |
| 3 | `design/tokens.css`, or a theme file | It defines custom properties or theme keys in use | Values |
| 4 | `brands/<slug>/` in the project or the kit | The pack holds `tokens.json` or `DESIGN.md` | Values and rules |
| 5 | `PRODUCT.md` or a brand guide file | It names audience, purpose and brand commitments | Brief input |
| 6 | A component library in the code | A UI package, a theme config or a components folder is in use | Components |
| 7 | A hosted design system | The user names one, or a read-only list call returns one | Values and rules |

Rules:

- Search the code for order 6. Look at the package manifest, the style config and the main stylesheet. Three greps are enough.
- For order 7, ask the user for the name or the link before any list call. A list call is read-only. It still shows account content, so make it only when the user works in that account.
- Two sources that disagree are a finding. Name both. Ask which one governs. Do not merge them in silence.
- A design system found in code but not written down is real. Route to `design-system` to record it before new work adds to it.
- When nothing is found, say "design system: none". Do not ask the user to write one. The flow creates it.

Classify what you found:

| State | Meaning | Effect on the plan |
| --- | --- | --- |
| `none` | No tokens, no rules, no library | The flow includes `mood-board` and `design-system` |
| `implicit` | A look exists in code, with no token file | `design-system` runs first, in import mode |
| `partial` | Tokens exist but a family is missing (motion, for example) | The discipline skill fills the gap and records it |
| `strict` | Tokens and rules cover the request | Skip `mood-board`, or run it with two directions that vary layout and imagery only |

## 2. Find the brief

1. Read the status line of `design/brief.md`, the first line under its title.
2. It is `confirmed` when the line starts `Status: confirmed YYYY-MM-DD by <who>`. The suffix `, ended early` still reads as confirmed: the user ended the interview, and the end counts as the yes. Read section 15 of the brief first in that case.
3. It is `draft` when the line reads `Status: draft`, or when any line is marked `(proposed)`.
4. It is `none` when the file is absent or reads `Status: template`.
5. Count the ASSUMED lines in section 15. Pass those that touch this request to the first skill.
6. Check that the brief covers this request: the same people, the same primary job, and a job size at least as large. A brief for the marketing site does not cover a new dashboard.

A brief that is `draft` or `none`, or that does not cover the request, sends the request back to `align`. Do not plan around it.

## 3. Read the decision record

1. Read the last three entries of `design/decisions.md`.
2. Note the stage of the last entry: explore, refine or finalize.
3. Note every `Rejected:` line that touches this request. Pass them to the first skill.
4. Note every `Open:` question. An open question that blocks this request goes to the user first.
5. When the last entry is recent and its scope matches, resume. Do not restart the flow.

## 4. List the tools present

The goal is a capability report, not a tool tour.

1. Read the file names in `kit/catalogs/tools/`. Open only the entries for the capabilities this request needs.
2. For each entry, read `toolPrefix`, `capabilities`, `spendsCredits`, `exposes`, `firstCall` and `fallback`.
3. A tool is present when a tool name in this session starts with its `toolPrefix`. Count deferred tool names too. For a `skill`, `plugin` or `cli` kind, check the skill list or the command.
4. Make no call to the tool at this point. Presence is read from the session's tool list.
5. A tool that is listed but needs sign-in is `needs sign-in`. Tell the user. Do not try to sign in.
6. A tool that failed to connect is `failed`. That is not the same as absent. Say so.
7. Local programs. When a needed capability appears in [local-clis.json](../../../catalogs/local-clis.json), run `python3 scripts/local_clis.py probe --capability <word> --json` from this skill's folder. It reads PATH and runs nothing it finds. A `ready` harness counts as a present tool. A `needs-harness` or `needs-backend` harness is an install offer for the plan, never an install. Card: [cli-anything](../../../references/tools/cli-anything.md).
8. For each needed capability, name the first tool present, in the order of the discipline's entry in `kit/catalogs/capabilities.json`. Default: when a ready local harness and a connector that spends both serve the capability, name the local harness first.
9. For a needed capability with no tool present, name the `fallback`, or the local harness to install. When neither exists, name the manual route: the agent writes the HTML, SVG or Markdown itself.

Report line:

```
Tools: image-gen (present, spends), vector (local: inkscape ready), 3d-scene (local: blender, offer install), capture (absent: ask for a screenshot), deploy (present, exposes)
```

Mark `spends` when `spendsCredits` is true. Mark `exposes` when `exposes` is true. An install offer is a gate too: the user says yes before any install. These marks feed the "Gates ahead" line of the plan.

Catalog absent or empty: say "tool catalog: none". Route by what the session lists, and label every tool claim UNTESTED.

## 5. Detect GCH

1. GCH is installed when the skill list holds a name that starts with `gch:`.
2. When the GCH kernel text is in context, GCH governs code work. Its `ux-laws` numbers hold for screens.
3. With GCH installed, use its skills at these steps:
   - Interview: `gch:grilling` runs the interview inside `align`.
   - Coded variants on one route: `gch:prototype`.
   - Offline boards for briefs, directions and reviews: `gch:placket`.
   - Screenshots before and after a change: `gch:browser-lane`.
4. With no GCH, `align` runs its own interview loop. Build variants as separate plain HTML files in `design/directions/`. Keep boards as local HTML or Markdown. Capture renders with a tool of the `capture` capability. With none, ask the user for a screenshot and label the check UNTESTED.
5. Do not ask the user to install anything unless they ask how.

## Report format

Give the pre-flight result to the first skill in this shape. The plan prints a shorter form.

```
Pre-flight
Design system: <none | implicit | partial | strict> at <paths>
Conflicts: <source A versus source B, or none>
Brief: <none | draft | confirmed> ; size <job size> ; covers this request: <yes | no> ; ASSUMED <n>
Decisions: last <date, scope, stage> ; rejected <n> ; open <n>
Capabilities needed: <list>
Tools: <capability (state, marks)> ...
GCH: <installed | absent>
Not checked: <what, labelled UNTESTED>
```

## Failure patterns

| Pattern | What goes wrong | Do this |
| --- | --- | --- |
| Template taken as a system | The agent finds the unfilled `DESIGN.md` template and reports "design system found" | Read the `status` line first |
| Tool tour | The agent calls every connector's guide tool "to see what it does" | Read catalog entries. Call a guide only inside the skill that uses the tool |
| Silent install | The agent installs a harness, or a whole CLI-Hub matrix, because the probe showed it missing | Print the pinned command and ask. One harness, only for this task |
| Ask before look | The agent asks the user for brand colors that sit in a theme file | Search first. Ask only for what no file answers |
| Silent merge | Tokens in two files differ and the agent averages them | Name the conflict and ask |
| Restart | A confirmed brief and a chosen direction exist, and the agent starts a new interview | `align` re-aligns in three questions. Resume from the last decision entry |

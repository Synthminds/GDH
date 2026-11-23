# Flows before screens

Read this file at steps 2 to 7 of `app-design`. It covers job stories, task ranking, the flow map, the screen inventory and the feasibility check with engineering. The output is the first half of `app-plan.md`.

Why this order. A screen drawn before its flow answers a question nobody asked. A flow drawn before the data is checked promises fields that do not exist. Both failures are cheap to prevent here and costly to fix after styling.

## 1. Job stories

A job story states a motivation in its situation. It is not a persona and not a feature.

Form: `When <situation>, I want to <motivation>, so I can <outcome>.`

Rules:

1. Each story has all three parts.
2. Each story comes from the brief, an interview, a support theme or the user's own statement. Mark any other story "assumption".
3. The situation is concrete: where the person is, what just happened, what is in their hands.
4. The story names no screen, no component and no technology.
5. Write the stories in the user's words. Collect those words in a short "user language" list and reuse them as labels.

| Weak | Why it fails | Stronger |
| --- | --- | --- |
| "As a user, I want a dashboard" | A feature, not a motivation. No situation | "When I open the app on site, I want to see which lifts are due today, so I can plan my route" |
| "When I use the app, I want it to be fast" | No job | "When I finish an inspection with one hand free, I want to log the result in a few taps, so I can move to the next lift" |

## 2. Rank the tasks

List each task behind the job stories. Rank by frequency, then by consequence.

| Task | How often | Consequence of failure | Rank |
| --- | --- | --- | --- |
| Example: log an inspection result | Many times a day | Lost work, repeat visit | 1 |
| Example: change notification settings | A few times a year | Annoyance | 9 |

Decision rules:

1. The most frequent task gets the shortest path and the most reachable control.
2. A rare task with a severe consequence gets the clearest path, with confirmation.
3. A task done many times a day gets no decorative step and no animation.
4. A task that nobody ranks in the top half is a candidate to cut. ASK before you design it.
5. Design the top three tasks first. Prove them in a prototype before the rest.

## 3. The flow map

Draw one map for each top task. A map is a path of steps with branches, not a set of screens.

Notation for a text map. Use it when no diagram tool is present. It also diffs well in a repository.

```
FLOW: Log an inspection result          (job story 1; frequency: many times a day)
ENTRY: Today list > tap a lift
1. Lift detail            [load: lift record]      on fail -> E1    empty -> n/a
2. Start inspection       [permission: camera]     denied  -> P1
3. Checklist              [save: each answer, local first]          offline -> O1
4. Add photo (optional)   [device: camera]
5. Review and submit      [write: inspection]      on fail -> E2
6. Confirmation           exit -> Today list, next lift highlighted
BRANCHES
E1  Record did not load: show cached copy with its age, offer retry
E2  Submit failed: keep every answer, queue for sync, say so
P1  Camera denied: continue without photos, explain how to allow later
O1  Offline: mark "saved on this device", show the sync state in the header
```

Mark on every step:

- What loads, and from where.
- What is written, and when.
- What can fail, be empty, be partial or be offline.
- Which permission or device feature the step needs.
- Where the person can go back, and what is kept when they do.
- How the flow ends. A flow ends on a confirmed finish, not on a blank screen.

Rules:

1. Name each step by the person's task, not by a table or an endpoint. "Review and submit", not "POST inspection".
2. Count the steps of the top task. Remove each step that carries no decision and no information.
3. Every branch ends somewhere useful. No dead end.
4. Put the map through a flow review before any styling. The review question is "can a person finish the job?".
5. For a diagram tool, pick by capability `diagram` or `whiteboard`. A text-source diagram can live in the repository.

## 4. The screen inventory

Derive screens from the flows. Do not start from a list of screens.

| Column | What to write |
| --- | --- |
| Screen | A name in the person's words |
| Job | The one thing the person does here |
| Used by flows | The flow ids that pass through |
| Entry points | Each way in: navigation, a link, a notification, a deep link |
| Exits | Each way out, including Back and cancel |
| Primary action | One. Others are quieter |
| Data shown | Field by field. This feeds the feasibility check |
| Data written | Field by field |
| States reachable | From the state matrix |
| Platform notes | What differs by platform |

Rules:

1. A screen with two jobs is split, or one job becomes a sheet or a step.
2. A screen that no flow passes through is cut.
3. A step that needs no full screen becomes a sheet, a popover or an inline edit. A modal is only for a task that must block.
4. The same screen on two platforms keeps its job. Its controls follow each platform.

## 5. The feasibility check

Gate: every data field, required form field and permission is confirmed with engineering before high-fidelity design.

The failure this prevents: a polished screen is cut apart late, because the data it shows does not exist, or a form misses fields the system requires.

Build one table from the inventory.

| Screen | Field or need | Kind | Question for engineering | Answer | Source of the answer | Design consequence |
| --- | --- | --- | --- | --- | --- | --- |
| Lift detail | Last inspection date | Shown | Does it exist for every lift? Can it be null? | Yes; null for new lifts | API schema, read on date | Design the "never inspected" state |
| Checklist | Photo per item | Written | Size limit? Offline upload? | Unknown | Asked the code owner | Open question. Photos stay optional |
| Today list | Distance to site | Shown | Is location available? | No | Code owner | Removed. Sort by due time |

Kinds: shown, written, required by the system, computed, permission, device feature, third-party.

Questions to ask for each field:

1. Does it exist today? In which source?
2. Is it present for every record? What does empty look like?
3. How fresh is it? Can it be stale?
4. How long does it take to load? Is it paged?
5. Who may see it? Does a permission or a role hide it?
6. For a form: which fields does the system require, with which formats and limits?
7. For a write: can it fail? Can it be undone? Is it safe to retry?

How to get the answers, in order:

1. Read the code, the API schema or the database schema when a repository exists. Cite the file.
2. With GCH installed, ask the coding harness for a feasibility pass.
3. ASK the code owner. One message, the whole table.
4. With no source, mark the row "unknown". An unknown row is an open question in `design/decisions.md`.

Decision rules:

- "No": remove the field, or redesign the screen without it. Do not keep it "for later" in a high-fidelity screen.
- "Unknown": design the screen so that it works without the field. Log the question.
- "Yes, sometimes empty": the empty case is a designed state.
- "Yes, but slow": the loading and partial states are part of the design.
- A technically risky element needs a working spike before you promise it: live data, heavy animation, a novel gesture, offline sync.

Agree on success measures with engineering at the same time: at least one quantity, such as task completion or load time, and at least one quality, such as a named design value.

## 6. Worked example

The subject is invented: an inspection app for lift technicians. Platforms: Android phones, plus a web app for the office. Brand words: steady, plain, quick.

- Job story 1: "When I finish checking a lift with one hand on the panel, I want to log the result in a few taps, so I can move on."
- Ranking: logging a result is rank 1. Viewing history is rank 4. Editing a profile is rank 9 and was deferred.
- Flow 1 has six steps. The first draft had nine. Three were removed: a "select inspection type" step that the lift record already answers, a summary screen that repeated the review step, and a rating prompt.
- Feasibility found two changes before any styling. "Distance to site" does not exist, so the list sorts by due time. The system requires a technician signature on submit, which the draft had missed, so step 5 gained a signature field.
- Offline is not an edge case here. Lift shafts have no signal. The flow saves on the device first, and the sync state is always visible.
- Open question logged: photo size limits for offline upload. Photos stay optional until it is answered.

## 7. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Screens first | A set of polished screens with no flow that links them | Stop. Write job stories and one flow map |
| Database navigation | Menu items are table names: Assets, Records, Entities | Rename from the job stories |
| Phantom field | A screen shows data that no source holds | Run the feasibility table |
| Missing required field | The build adds form fields that the design never showed | Ask for the system's required fields early |
| Happy flow | The map has no fail, empty or offline branch | Mark each step |
| Dead end | A branch ends on a message with no next step | Give every branch an exit |
| Equal weight | The rare task and the hourly task have the same path length | Rank, then shorten the frequent path |
| Decorated build | Design arrives after the build and only restyles it | Review the flow first, with the person's tasks |

## 8. Checks

Gates:

- Each top task has a job story with three parts and a flow map with fail, empty and permission branches.
- The screen inventory exists, and each screen has one job.
- Each row of the feasibility table has an answer and its source, or is a logged open question.
- The user answered keep, change or remove on the gray-box flows.

Defaults:

- Default: design and prove the top three tasks first.
- Default: one primary action on a screen.
- Default: four choices at one decision point.

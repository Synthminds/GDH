# Dashboard type, audience and decisions

Read this file at steps 1 and 2 of `dashboard-design`. It covers the three dashboard types, how to tell them apart, the audience interview, look frequency and context of use, and the questions that turn a request into a brief.

Evidence. The definition of a dashboard as a single-screen display read at a glance, and the separation of monitoring from exploration, come from Stephen Few, "Information Dashboard Design", known through a book review (search summary). The overview-filter-details order is Shneiderman (1996, from memory). The rule that default views of volatile data must not provoke panic comes from Aarron Walter, "Designing for Emotion", chapter 6. The four-principles check comes from the Design Engineering Handbook, chapter 2. All numbers are defaults.

## 1. Settle the type first

| | Monitoring | Analysis | Report |
| --- | --- | --- | --- |
| Job | Notice a change and act | Find out why, compare, explore | Read a fixed account of a period |
| Read | At a glance, often, often on a second screen | In sessions, with interaction | Once, start to finish |
| Time | Now and recent; live or near-live | Any period the analyst picks | A closed period |
| Interaction | Little or none; drill to act | Filters, drill-down, comparison, export | Little; maybe a period picker |
| Layout | One screen, no scroll; status first | Overview, then detail panels; may scroll | Top to bottom, like a document; may print |
| Density | Low to medium; large status | Medium to high | Medium; prose plus charts |
| Main risk | Alarm fatigue; missed alerts | Tool sprawl; no default answer | Charts without a story |
| Typical users | Operators, support leads, on-call engineers | Analysts, product managers | Executives, boards, clients |

Rules:

- One type per screen. A screen that tries to monitor and explore does both badly. Split it: a monitoring screen that links to an analysis view.
- When the request is unclear, ask: "Will people watch this during the day, dig into it to find causes, or read it once a month?"
- A report can be a page, a PDF or a data story. A monitoring screen can be a wall display or a phone card. Record the device and screen size with the type.

## 2. Audience and decisions interview

Ask in this order. Record each answer in `dashboard-plan.md`.

1. Who looks at this screen? Name roles, not "everyone".
2. What decisions do they make from it? Each decision is a verb: "reassign agents", "pause the campaign", "call the client".
3. What do they do when a number is bad? If the answer is "nothing", the number belongs in a report, not on a monitor.
4. How often do they look? Every few minutes, daily, weekly, monthly.
5. Where and on what? A desk monitor, a wall screen across a room, a laptop in a meeting, a phone between tasks.
6. What do they compare against? A target, last week, last year, a peer group, a forecast.
7. What do they already use? An existing report, a spreadsheet, a vendor screen. What is wrong with it?
8. Who owns each number? Who will answer "why is this wrong"?

Write a one-line purpose: "This <type> screen lets <role> <decision> by showing <what>, <how often>."

## 3. Look frequency and context change the design

| Context | Design consequence |
| --- | --- |
| Glanced every few minutes on a second screen | Status first; large type; color only for exceptions; no interaction needed to know the state |
| Wall display across a room | Default: very large numbers and labels; no hover; no small text; high contrast; auto-refresh with a visible data time |
| Daily check at a desk | Top-left summary; comparison to yesterday and to target; links to detail |
| Weekly or monthly review in a meeting | Narrative order; a one-sentence summary at the top; printable |
| Phone between tasks | One column; the three most important tiles; no hover; large targets |
| Infrequent use by design (long-term decisions) | Long default ranges; contributions or progress first; volatility behind a control |

Rule from "Designing for Emotion": for volatile data used for long-term decisions, choose a default range that supports good decisions. Do not default to the range that looks most alarming. Keep other ranges one click away.

## 4. Check the four principles

Before layout, answer each in one line (Design Engineering Handbook, chapter 2):

- Value: which user problem does this screen solve?
- Usability: can the named users read it and act without training?
- Feasibility: do the data sources exist, at the needed refresh rate and permission level?
- Viability: what business outcome improves when people use it?

A "no" on feasibility stops layout work. Ask for the data, or change the scope.

## 5. Outcomes per user type

Write one outcome per user type, not one blended goal.

```
Support lead: notices a queue backlog within 10 minutes and reassigns agents.
Head of support: sees in the weekly review whether response time met target, and why not.
```

These outcomes become the user tasks for the test in step 16.

## 6. Signals that the request is not a dashboard

| Signal | Better route |
| --- | --- |
| One chart with one finding | `data-viz` |
| A fixed message for an outside audience | `infographic` |
| Most actions change data (edit, approve, assign) | `app-design`, with read views inside it |
| The user wants to "see everything" with no decisions named | Run the interview again; propose an analysis view with a short default |
| Relationships between entities are the story | `network-graph` |

## 7. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Type soup | Live alerts, ad hoc filters and a monthly narrative on one screen | Split by type; link between them |
| Data-first design | "We have these 40 fields, show them" | Decisions first; metrics only for decisions |
| No owner | Nobody can say why a number moved | Owner column in the inventory; ask before layout |
| Panic default | A volatile measure shown at the noisiest range | Default range chosen for the decision; noise behind a control |
| Built for the builder | Dense analyst screen for an executive audience | Type and density from the audience interview |

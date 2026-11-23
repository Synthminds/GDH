# Questions, the metric inventory, comparisons and time range

Read this file at steps 3 to 6 of `dashboard-design`. It covers turning decisions into questions and metrics, the inventory format, definitions and sources, cut rules, comparisons and targets, the default time range, ranking, and failure patterns.

Evidence. "Map each question to one metric, cut metrics with no question, give each metric context" comes from the dashboard section of the GDH research, based on Stephen Few (search summary). Plain-word definitions beside the figure, signed change with a comparison window, and coloring change by good or bad come from the Claude Data type design defaults (read 2026-11-23). The default-range rule comes from "Designing for Emotion", chapter 6. The four-item and five-to-nine limits are the GDH resolution of conflicting sources; both are defaults.

## 1. From decisions to questions to metrics

1. Take each decision from the audience interview.
2. Write the question a person asks before that decision: "Is the queue growing faster than we close tickets?"
3. Name the one metric that answers it: "Open tickets, now, with change over the last hour."
4. Name the comparison that tells good from bad: target, prior period, trend or peer.
5. Name the action when it is bad: "Reassign two agents from email to chat."

A metric with no question is cut. A question with no metric is a data gap: record it and ask the owner.

## 2. The inventory

Keep one row per metric in `dashboard-plan.md`. Every column is filled before layout.

| Column | Content | Example |
| --- | --- | --- |
| Metric | Reader name | First-response time |
| Question | The question it answers | Are customers waiting too long for a first reply? |
| Decision | The action it informs | Add staff to the morning shift |
| Definition | Plain words | Time from ticket creation to the first human reply, business hours only |
| Formula | Exact computation | Median of (first_reply_at - created_at) over tickets created in the window |
| Unit and precision | Unit, rounding | Minutes, whole numbers |
| Source | System, table, query or connector | Help desk export, `tickets` table |
| Owner | Who answers "why did it move" | Support operations lead |
| Refresh | How often the data updates | Every 15 minutes |
| Comparison | What it is compared to | Target 60 min; same hour last week |
| Good direction | Up or down is good | Down |
| Window | Default period | Today, by hour |
| Thresholds | When it becomes a warning or alert, if any | Warning above 60, alert above 120 |
| Caveats | Known limits | Excludes tickets created by API |
| Priority | Rank on the screen | 1 |

Rules:

- Use the formula's real filters in the definition. A reader trusts a number they can explain.
- Use medians or percentiles for skewed measures like time; say which.
- Record a threshold only when someone owns the response to it. An alert nobody acts on trains people to ignore alerts.
- Never invent a target. When no target exists, use a prior period or a trend, and record "no target set".

## 3. Cut rules

Cut, or move to a detail view, every metric that:

- answers no written question;
- informs no decision on this screen's cadence;
- duplicates another metric (two measures of the same thing);
- cannot be trusted yet (source unknown, definition disputed): show a labelled data gap instead;
- exists only because the data is available.

Record each cut and its reason in `design/decisions.md`. Cut metrics often return as requests; the record answers them.

Budget:

- Default: four items at one decision point (a group of tiles read together).
- Default: five to nine headline metrics on one screen is the ceiling. More belongs in a detail view or a second screen.

## 4. Comparisons and context

Every headline metric shows at least one comparison. A number alone says little.

| Comparison | Use when | Show as |
| --- | --- | --- |
| Target or budget | A goal exists and is owned | Bullet bar, or "62 of 75 target" |
| Prior period | Change matters: day over day, week over week | Signed change with the window: "+12% vs last week" |
| Same period last year | Strong seasonality | "+4% vs same week 2025" |
| Trend | Direction over time matters more than one value | A sparkline of the window, last point marked |
| Peer or benchmark | Fair comparison groups exist | Rank or percentile with the group named |
| Forecast | A plan or a model exists | Actual against forecast band |

Rules:

- State the comparison window in words on every tile: "vs last 7 days".
- Color the change by whether it is good for the goal, not by its sign. Fewer complaints is good, even though the number fell.
- Show a signed change and its absolute value when the base is small: "+50% (from 4 to 6)".
- When a comparison period is incomplete (this week so far), compare to the same elapsed part of the prior period, and say so.

## 5. Choose the default time range on purpose

The default range is a design decision. Write the reason in `dashboard-plan.md`.

| Situation | Default range | Reason |
| --- | --- | --- |
| Live operations | Today, by hour, with the last few hours prominent | The decision is about now |
| Daily management | Last 7 or 28 days, by day | Smooths weekday effects; shows the trend |
| Weekly review | Last 13 weeks | A quarter of context with recent weeks clear |
| Monthly or board report | The closed month, with the same month last year and the year to date | Comparable, complete periods |
| Long-term decisions on volatile data | A long range, with the reader's contribution or goal first | A short volatile window provokes panic and bad decisions |

Rules:

- Use complete periods for comparison when you can. A partial current period is labelled "to date".
- Keep other ranges one click away, and show the active range in the header.
- Use the same range across all tiles of the screen unless a tile says otherwise.

## 6. Rank and group

1. Rank metrics by the importance of their decision and how often it is made.
2. Group metrics that answer related questions (all queue health together; all quality together).
3. Within a group, order from summary to detail: the headline, then its breakdown.
4. Mark the one metric that answers "is anything wrong right now?" for a monitoring screen. It goes first in the reading order.

## 7. The one-sentence summary

Under the screen title, write one sentence that says what the numbers say now, filled from the data: "Response time is within target; the chat queue grew 30 percent in the last hour." A report always has one; a monitoring screen can use a status line instead.

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Metric dump | Thirty tiles because the fields exist | Questions first; cut rules; detail views |
| Naked number | "4,812" with no comparison | Target, prior period or trend on every headline |
| Sign as color | A fall in costs shown in red | Color by good or bad for the goal |
| Undefined metric | Two teams compute "active user" differently | Definition and formula in the inventory, shown where the metric first appears |
| Invented target | A goal line nobody set | "No target set"; use a prior period |
| Alarm without owner | A red threshold nobody acts on | Threshold only with an owned response |
| Partial-period trap | This week so far compared to all of last week | Same elapsed period, labelled |

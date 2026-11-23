# Worked example: a support operations monitor

Read this file to see the whole `dashboard-design` procedure on one case. The company, metrics and numbers are invented for illustration. Nothing was rendered. Evidence: UNTESTED.

The request: "We need a dashboard for the support team. Show everything from the help desk."

## Steps 1 and 2. Type, audience and decisions

The interview found two audiences with different cadences. The request split into two screens.

| Audience | Decisions | Cadence | Type |
| --- | --- | --- | --- |
| Shift leads (4) | Move agents between chat and email; escalate a spike | Every few minutes, second monitor | Monitoring |
| Head of support | Staffing plan; process changes | Weekly review meeting | Report (built later) |

Purpose: "This monitoring screen lets shift leads rebalance agents by showing queue health by channel, every few minutes."

Device: a 1920 by 1080 monitor beside the help desk; a phone card for on-call leads.

## Steps 3 to 6. Questions and the inventory

| Question | Metric | Comparison | Good direction |
| --- | --- | --- | --- |
| Is anyone waiting too long right now? | Longest current wait, by channel | Threshold: warning 10 min, alert 20 min (owned by shift lead) | Down |
| Is the queue growing? | Open conversations, by channel, with change over the last 30 minutes | Same 30 minutes last week | Down |
| Are we answering fast enough today? | Median first-response time, today | Target 5 min chat, 60 min email | Down |
| Do we have enough people on each channel? | Agents online, by channel | Planned staffing for this hour | Up to plan |
| What needs action? | Conversations over the alert threshold, with age and assignee | None; it is a list | Fewer |

Definitions written in the inventory, for example: "First-response time: time from a customer's first message to the first human reply, in business hours; excludes conversations closed by automation."

Cut, with reasons recorded:

- Satisfaction score: weekly decision, not a shift decision. Moved to the weekly report.
- Tickets by product area: no shift decision uses it. Moved to the report.
- Agent leaderboard: no decision on this screen; risk of misuse. Cut.

Default time range: "Today, by 15 minutes, with the last 2 hours prominent." Reason: the decision is about now; a full-day trend gives context for the morning peak.

## Step 7. Reading order

1. Status line: "Chat wait over threshold; email on target."
2. Headline group by channel: longest wait, open conversations, agents online versus plan.
3. Main chart: open conversations through today, chat and email, with last week's same day as a light reference line.
4. Exceptions list: conversations over 20 minutes, oldest first.
5. Today's median first response against target, as bullet graphs.

## Steps 8 and 9. Tiles, displays, color

- Each channel group has three tiles. Example tile:

```
Chat: longest wait                         now
14 min                          Warning (icon + word)
+6 min vs 30 minutes ago
[bullet bar against the 10 and 20 minute thresholds]
```

- Open conversations: line chart through today; last week as a reference line in the context gray; current value labelled at the line end.
- Agents online versus plan: a pair of numbers per channel, "6 of 8 planned", with the gap as a word when short.
- Exceptions: a table with customer, channel, age, assignee; age right-aligned, tabular; rows over 20 minutes carry "Alert" plus icon.
- Color: neutral screen; status colors only on threshold crossings; chat and email as two data colors used the same way in every view.
- Density: medium-high for experienced leads; numbers large enough to read at arm's length.

## Step 10. Gray-box round

Shown with real names and yesterday's numbers. Feedback:

| Block | Keep, change or remove |
| --- | --- |
| Status line | Keep |
| Agents versus plan | Change: put it beside the queue, not below |
| Main chart | Keep; add a marker for "now" |
| Exceptions | Change: add "time in current status" |
| First response bullets | Remove from the monitor; move to the report |

Logged in `design/decisions.md`. Only these changes were made.

## Steps 11 and 12. Filters and states

- Filters: none on the monitor except a team selector (persisted in the URL). The default answers the shift's question.
- Data time: "Updated 14:32 CET; refreshes every minute". Stale after 5 minutes: the stamp turns to a warning with the word "Stale".
- States designed: loading (skeleton of the final grid), no data (night shift with closed chat: "Chat closed until 07:00"), stale, partial (email source failed: chat views remain, email views show an in-place error), error, no permission (contractors see their team only; totals say so), filtered to nothing.

## Step 13. Route

Code route. The dashboard opens beside the help desk inside the company's internal tools app; a data page cannot ship there. The existing chart library is reused; the host chart skill was loaded for mark and palette checks.

## Steps 15 and 16. Build and test

- Real data at production size: 1,900 conversations on the busiest day of last month.
- Edge cases rendered: empty chat channel, one conversation waiting 3 hours, a 60-character customer name, the email source down.
- Glance test with two shift leads: both named "chat needs people" within five seconds.
- User task: "Rebalance agents when chat wait passes 10 minutes." Both completed it in under a minute.
- Values: five numbers recomputed from the help desk export; all matched.
- Keyboard: team selector, exceptions table sort and row links reachable with visible focus.

## Closing report

```
Dashboard: support operations monitor; type monitoring; route code
Users and decisions: shift leads rebalance agents between chat and email
Metrics: 4 of 7 proposed (3 moved to the weekly report); defined and sourced 4/4; with comparison 4/4
Default range: today by 15 minutes, because decisions are about now
States: 7/7 designed
Data: real, production size; data time shown yes
Glance test: 2 of 2 named the status; user task: 2 of 2 completed
Evidence: UNTESTED (illustrative example)
```

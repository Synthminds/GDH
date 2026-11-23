# Every state

Read this file at step 12 of `app-design`. It defines the states a screen can be in, the rule for each, the state matrix, the feedback tiers and the words each state needs.

A screen is not one picture. It is a set of states, and people spend real time in the unhappy ones. A state that nobody designed is designed by accident, usually as a blank area or a raw error string.

## 1. The seven core states

| State | The person's question | Design rule |
| --- | --- | --- |
| Empty | "Is something wrong, or is there nothing yet?" | Say what will appear here and why it is empty. Offer the next action |
| Loading | "Is it working?" | Show the shape of what is coming. Keep the layout still |
| Partial | "Is this all of it?" | Show what loaded. Mark what is missing and whether it is still coming |
| Error | "What happened, and what can I do?" | Say what failed, in plain words. Offer a way forward. Keep the person's work |
| Success | "Did it work?" | Confirm the result where the person is looking. Say what happens next |
| Offline | "Can I keep working?" | Say what works without a connection. Show what is saved on the device and what waits to sync |
| Permission | "Why can't I do this?" | Say what is blocked and why. Say who or what can unblock it |

Further states. Add each one that the screen can reach.

| State | When it applies | Rule |
| --- | --- | --- |
| First run | The first visit, before any data exists | Teach by doing the first real task, not by a tour |
| Stale | Data is older than the person expects | Show the age of the data. Offer refresh |
| Not found | The item was deleted or the link is wrong | Say so. Offer the nearest useful place |
| Too much | A list or a value far beyond the sample | Page, virtualize, group or summarize |
| Limited | A quota, a rate limit or a plan limit was reached | Say what was reached, when it resets and what to do |
| Disabled feature | The plan, the role or a flag turns it off | Explain it, or do not show the control |
| Conflict | Another person or device changed the same thing | Show both versions. Let the person choose |

## 2. Three kinds of empty

"Empty" covers three different situations. Each needs different words.

| Kind | Example | What to show |
| --- | --- | --- |
| Nothing yet | A new account with no records | What belongs here, and one action that creates the first item |
| Nothing matches | A search or a filter with no result | The active filters, and one tap to clear them |
| All done | An inbox or a task list at zero | A plain confirmation. This is a success, so say it like one |

Never show a blank area. Never show the same illustration and the same line for all three.

## 3. Loading

| Wait | Default treatment | Class |
| --- | --- | --- |
| Up to about 100 ms | Nothing. It reads as instant | Memory: Nielsen Norman Group response-time limits |
| Up to about 1 s | A subtle busy sign on the control or region. No layout change | Memory: same source |
| More than about 1 s | A skeleton that matches the final layout, or progress in place | Read: Vercel, for the skeleton rule |
| More than about 10 s | Real progress, a way to cancel, and permission to leave and come back | Memory: same source |

With GCH loaded, its single feedback number governs for screens. This table is the GDH teaching model.

Rules:

1. A skeleton matches the final layout, so nothing shifts when content arrives.
2. Do not flash a loader on a fast path. Delay it a little, then keep it long enough to read. Set both values as motion tokens.
3. Load the frame first, then each region. One slow region must not block the rest.
4. A button that starts work keeps its label and its width, shows that it is busy, and blocks a second press.
5. For a write, update the screen at once when the result is near certain, and roll back with a clear message when it fails.
6. A number that is still loading is never shown as zero.

## 4. Error

Sort the error first. Each kind has a different remedy.

| Kind | Example | Remedy on screen |
| --- | --- | --- |
| The person can fix it | A bad format, a missing field | Inline, beside the field. Name the fix |
| A retry may work | A timeout, a dropped connection | Keep the work. Offer retry. Queue it when offline |
| The person cannot fix it | A server fault, a bug | Say it is not their fault. Offer a way to save or leave safely. Give a reference for support |
| It is not allowed | A role or a plan limit | Treat it as the permission state |
| The data is wrong | A corrupt or unexpected record | Show what can be shown. Mark the broken part |

Rules:

1. Gate: an error keeps the person's input.
2. Write the message in the person's words. No codes alone, no stack text.
3. Put the message where the problem is. A banner at the top is for a problem with the whole screen.
4. Announce the error to assistive technology with a polite live region.
5. Color alone does not mark an error. Add an icon and words.
6. A partial failure does not blank the screen. The parts that worked stay.

## 5. Success and destructive actions

- Confirm a success where the person is looking: the item appears in the list, the button settles, a short message names the result.
- A message that disappears by itself stays long enough to read and is also reachable later. Do not put the only copy of important information in it.
- A flow ends on a confirmed finish and offers the next likely task.
- Gate: a destructive action asks first or offers undo. Prefer undo for frequent, low-risk actions. Prefer a confirmation that names what is lost for rare, high-risk ones.
- The confirm button names the action: "Delete 3 inspections", not "OK".

## 6. Offline and sync

Decide the offline level for each flow, with engineering, in the feasibility check.

| Level | The person can | The design shows |
| --- | --- | --- |
| None | Only read a message | What needs a connection, and a retry |
| Read | See the last loaded data | The age of the data |
| Queue | Do the work; it sends later | "Saved on this device", a pending count, the sync result |
| Full | Work normally for long periods | Sync state, conflicts and their resolution |

Rules:

1. Show the connection state only when it changes what the person can do.
2. Every item that waits to sync is marked. The mark clears when the item is sent.
3. A failed sync says which item failed and keeps it.
4. Never show queued work as done on the server.

## 7. Permission

Two cases share this state.

| Case | Example | Rule |
| --- | --- | --- |
| A device permission | Camera, location, notifications | Ask at the moment of need, after the person starts the task. Say what it is for first. Design the denied path: the task continues without it, or the screen says how to allow it later |
| An account permission | A role, a plan, a locked record | Say what is blocked and who can change it. Do not show a control that can never work without an explanation |

A denied permission is not an error. Do not ask again on every screen.

## 8. The state matrix

Fill one row for each screen and each region that loads on its own.

```
Screen or region | Empty | Loading | Partial | Error | Success | Offline | Permission | Other
Today list       | all done; nothing yet | skeleton rows | n/a | retry + cached copy | n/a | cached, with age | n/a | stale: age shown
Checklist        | n/a | skeleton | answers saved, photos pending | keep answers, queue | saved mark per item | saved on device | camera denied | conflict
```

Rules:

1. Write "n/a" only with a reason you can state. "It cannot fail" is rarely true.
2. Each cell names the treatment in a few words and links to its frame or component.
3. Every theme has every state. Check the unhappy states in dark mode; they are the ones most often missed.
4. The matrix goes into the handoff as it is. It is the list of what the build must implement.
5. Count the cells. Report designed over reachable in the closing report.

## 9. State copy

Write the words with the screen, not after it.

| State | Pattern | Example |
| --- | --- | --- |
| Empty, nothing yet | What belongs here + first action | "No inspections yet. Start with a lift from Today." |
| Empty, no match | What was searched + how to widen | "No lifts match 'Harbor'. Clear the filter." |
| Loading, long | What is happening + what the person can do | "Preparing the report. You can leave this screen; we will notify you." |
| Error, retry | What failed + that work is kept + action | "Could not send. Your answers are saved on this device. Try again." |
| Error, not theirs | Plain fault + safe next step | "Something failed on our side. Your work is saved. Try again in a few minutes." |
| Offline | What still works | "You are offline. Inspections are saved here and will send when you reconnect." |
| Permission, device | What for + how to continue | "Camera access is off. You can finish without photos, or allow it in Settings." |
| Limit | What was reached + reset + action | "You reached today's export limit. It resets at midnight." |

Rules: plain verbs, no blame, no apology loops, no jokes in an error. One name for each thing through the whole app.

## 10. Worked example

The invented inspection app, the Checklist screen.

- Empty does not apply: a checklist always has items. Reason stated in the matrix.
- Loading: skeleton rows in the shape of checklist items. The lift name in the header loads first.
- Partial: answers are saved; two photos are still uploading. Each photo shows its own progress. The submit button stays enabled, because photos are optional.
- Error on submit: every answer stays. The message says the work is saved on the device and will send later. The item appears in a "waiting to send" count on Today.
- Offline: the normal case in a lift shaft. No banner shouts. A small "saved on this device" mark sits on each answered item.
- Permission: camera denied. The photo control explains what it is for and how to allow it. The inspection can still be finished.
- Conflict: the office edited the same lift record. The technician sees both versions of the changed field and picks one.
- Finding from the matrix: the first design had no state for "signature missing". The system requires one, so the review step gained an inline error.

## 11. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Happy path only | One picture of each screen, full of ideal data | Fill the matrix |
| Blank empty | A white area where a list would be | Say what belongs here and offer the action |
| Spinner page | A full-screen spinner for a partial load | Frame first. Skeleton by region |
| Loader flash | A loader that appears for a blink | Delay it. Give it a minimum time |
| Zero while loading | "0" shown before the number arrives | A skeleton or a dash, never zero |
| Raw error | A code or a stack line shown to the person | Sort the error. Write the remedy |
| Lost work | An error or a Back press clears the form | Keep the input |
| False done | Queued work shown as sent | Mark it pending until it is sent |
| Permission wall | A permission prompt on first launch, before any task | Ask at the moment of need |
| Dead control | A button that never works for this role, with no reason given | Explain it or remove it |

## 12. Checks

Gates:

- Every screen has each reachable state designed, in every theme.
- An error keeps the person's input. A destructive action asks first or offers undo.
- No state shows invented or queued data as real and final.
- No state marks its meaning by color alone.

Defaults:

- Default: the wait tiers in part 3: about 100 ms, about 1 s, about 10 s.
- Default: a skeleton for a wait over about 1 s.
- Default: ask for a device permission at the moment of need.
- Default: undo for frequent low-risk actions; confirmation for rare high-risk ones.

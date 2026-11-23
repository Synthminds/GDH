# Exercise the tool and set the evidence label

Read this file at steps 8 to 11 of `add-design-tool`. It covers the connection step, the first real call, the spend and exposure gates on that call, and how the evidence label is set and lowered.

Evidence. The labels are the kit principles' own. The "one free read-only smoke test" and "connected only after a real call succeeds" rules come from the owner's field guide on mapping MCP servers and the GCH run-once gate, read through the GDH research: DOCUMENTED as method.

Terms. A smoke test is one free, read-only call that proves the tool exists in the session and answers. A spend call uses credits or a paid quota. An exposure call publishes, shares, uploads or sends.

## 1. Connect

GATE: connecting a server or signing in is the user's step.

1. Give the user the steps from the card's "Connection and auth" for their host.
2. Ask them to restart the host or start a fresh session after a config change.
3. Never ask for a token in chat. A key goes in the host's settings or an environment variable the user sets.
4. When the tool still does not appear, check the host's connector list with the user. A listed but unauthorized tool is not connected.

When the user cannot connect it now, keep the entry DOCUMENTED and say what remains.

## 2. The first call

The goal is to prove one thing: the tool exists in this session and answers.

1. Confirm the tool appears in the session's tool list under its `toolPrefix`.
2. Call its guide or init call first, when it has one. Some tools refuse other calls before it.
3. Pick a free read: a guide, a list of templates, a list of models, a usage or balance call, a search.
4. Read the result. Note its shape, any limit it states, and anything that asks for money or an upload.
5. Write the call, the date and the outcome into `evidenceNote` and the card's Evidence section.

Order of preference for the smoke test:

| Rank | Call kind | Example |
| --- | --- | --- |
| 1 | Guide or init | The call the card names as first |
| 2 | List or search | Templates, presets, the user's own files |
| 3 | Usage or balance | Shows the cost model works; never write the number |
| 4 | Dry run or quote | A call that quotes without spending |
| 5 | A real job | Only with a yes, see section 3 |

## 3. Spend and exposure on the first call

GATE: a spend call is made only after a live quote and the user's yes. Then call once.

1. Read the balance. Get a quote. Show both. Ask.
2. On a yes, call once. On a timeout, read the job state. Never repeat the call blind.
3. Without a yes, test only free reads. The paid path is recorded as "not exercised".

GATE: an exposure call needs a yes that names what leaves and where it goes. Test with a harmless file the user supplies, never client material.

## 4. Labels

| Label | Means | Example note |
| --- | --- | --- |
| VERIFIED | A real call ran in a session and the note names it | "Init and template search ran on 2026-11-23. The conversion call was not run." |
| DOCUMENTED | Read from the publisher's pages or the tool's own description; nothing was called | "Guide page and call descriptions read. No call made." |
| UNTESTED | Stated by a third party, or recalled from memory | "From a vendor blog. Source page not opened." |

Rules:

1. The entry gets the label of the weakest claim a skill relies on.
2. VERIFIED covers only what ran. The same note says what did not run.
3. Reading more text never makes a claim VERIFIED.
4. A label goes down as well as up. A tool that stopped answering returns to DOCUMENTED, with the date.
5. A number from today's quote is still not written into a file.
6. Skills treat an UNTESTED fact as a default, never as a gate.

## 5. What to write

`evidenceNote`, one paragraph:

```
Init and preset list ran on 2026-11-23; both answered. The conversion call was not run (spend, no yes). Upload behavior read from the privacy page only. Local CLI path not installed.
```

Card, Evidence section:

```
VERIFIED on 2026-11-23: init call, preset list.
DOCUMENTED: conversion output format and link lifetime, from the call descriptions.
Not exercised: conversion (spend), batch mode.
```

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Label inflation | VERIFIED with no call named | Lower the label; write what ran |
| Test by spending | A paid job run "to see if it works" | Free read first; quote and yes for the rest |
| Blind retry | A second job after a timeout | Read the job state first |
| Client file as test input | Real client material uploaded in a test | Use a harmless sample the user supplies |
| Listed equals connected | The tool shows in a list but every call fails auth | Ask the user to sign in; keep DOCUMENTED |

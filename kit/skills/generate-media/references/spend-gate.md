# The spend gate in full

Read this file at steps 10 to 13 of `generate-media`. It covers the spend gate step by step, the quote mechanisms tools offer, the one cheap test before a batch, timeouts and job state, request keys, the project spend ledger, and what to say to the user at each point.

Evidence. The gate is kernel rule 5. The mechanisms come from the connector cards, read from schemas and guides on 2026-11-23: a cost estimate that returns a quote reference to pass to the generation call; a dry-run flag that returns credits for edits and model jobs; an estimate-only flag on generation calls; a heads-up sentence some tools require before a call that uses a monthly allowance; request keys where a retry with the same key is safe and a new key is a new charge; and tools that report no balance at all. No spend call ran in research. Prices, balances and allowance rules change; read them live.

## 1. Which calls spend

A call spends when the tool's card or description says it does. Typical spend calls:

- Generate an image, a clip, speech, music, an effect or a model.
- Edit a generated output: upscale, background removal, expand, retexture, remesh.
- Some analysis calls: video analysis, transcription in some tools.
- Renders in hosted video tools.
- Licensing a stock asset.

Typical free calls: guides, model lists, quotes and estimates, balances, job status, listing past results. Read the card; do not assume.

## 2. The gate, step by step

1. Read the balance. Use the tool's balance call. When the tool reports none, ask the user to confirm the balance in their account, and say so.
2. Get a quote for the exact job: model, count, size, length, quality. Use the tool's quote, estimate-only or dry-run call.
3. Compute the running total against the project spend limit, from the ledger.
4. Show the user, in one short block:

```
Spend check
Job: 2 test images, <model read live>, 4:3, standard quality
Quote: <n> <units> (from the tool's estimate)
Balance: <n> <units>
Project so far: <n> of a <limit> limit
Proceed? (yes / change / no)
```

5. Get a yes for this job. A yes for an earlier job does not carry over.
6. Call once. Pass the quote reference or a new request key when the tool supports one, so the run matches the quote.
7. Keep the job id. Write it in the prompt log before polling.
8. Poll at the interval the card gives. Do not poll faster.
9. When done, download each result at once.
10. Record the charge when the tool reports it. Update the ledger.

Some tools require their own fixed heads-up sentence before a call that uses a monthly allowance. Say it exactly when the card says so, then wait for a new explicit yes.

## 3. One cheap test before a batch

1. The test answers one question: does this prompt, kit and model give the look?
2. Use the smallest useful job: one or two outputs, the cheapest quality that shows the look, the shortest clip length.
3. Review the test with the user before any batch.
4. Fix the kit or the prompt, and test again when needed. A second test is still cheaper than a bad batch.
5. Then quote the batch as one job and run the gate again.

Default: a test is one to two outputs. A look test across directions is two to four outputs.

## 4. Set the count

Several tools default to more than one output per call (several variations of an image, several takes of a line). Each output may spend.

1. Set the output count explicitly on every call.
2. Default: one output per prompt for a batch of distinct prompts; two for a look test of one prompt.
3. Show the count in the spend check.

## 5. Timeouts, errors and retries

A spend call that times out may still run and charge. A blind retry can pay twice.

After a timeout or an unclear error:

1. Do not call again.
2. Read the job state with the job id. When there is no id, list recent jobs or generations.
3. When the job is running, wait and poll.
4. When it finished, use its result.
5. When it failed, read the reason. A failed run may not be charged; the card says.
6. Retry only with the user's yes.
7. When the tool uses request keys, retry with the same key. A new key is a new job and a new charge. When the tool uses quote references, a retry needs a fresh quote.

| Error | Do |
| --- | --- |
| Insufficient credits | Stop. Tell the user the quote and the balance. Do not retry until they say they are ready. |
| Rate limit | Wait as the tool says. The refused call was not run. Retry once after the wait, with the user's earlier yes still valid for the same job. |
| Safety or IP refusal | Do not rephrase to get around it. Tell the user; change the prompt sheet if it caused the refusal. |
| Invalid parameters | Read the live schema. Fix the call. Quote again if the job changed. |
| Timeout | Read the job state, as above. |

## 6. Cancellation

1. Some jobs cannot be cancelled once started (several 3D jobs). Say so in the spend check.
2. When a tool offers cancel, it may not refund. Read the card.

## 7. Spend in hosted flows

1. A tool's own multi-step flow (a website build, a brand kit, an ad set) may make many spend calls. Ask the tool's flow for its total, or estimate the steps, before starting.
2. Run the gate for each paid step the flow exposes, unless the user approved a total budget for the flow. Track against it.
3. Paid GPU rental bills by time until stopped. Stop it as soon as the job ends. Confirm it stopped.

## 8. The project spend ledger

Keep it at the top of `prompt-sheet.md`:

```
Spend ledger (units as the tool reports them)
Limit: <n>, set by <user> on 2026-11-23
| Date | Tool | Job | Quote | Charged | Job id | Approved by |
| 2026-11-23 | <tool> | 2 test images | <n> | <n> | <id> | user |
| 2026-11-23 | <tool> | 4 batch images | <n> | <n> | <id> | user |
Total charged: <n>
```

Rules:

1. One ledger per project, across tools. Different tools use different units; keep a row per tool and do not add units across tools.
2. Warn the user when the next quote would pass the limit. Never pass it without a new yes.
3. The ledger is project data. It holds no balance of the user's account in a public repository; balances stay in the chat.

## 9. What never happens

- No spend call without a quote shown and a yes for that job.
- No retry after a timeout without reading the job state.
- No new request key on a retry of the same job.
- No opt-in allowance, free-generation flag or unlimited mode used without the user choosing it.
- No paid edit or upscale of an output the user did not select.
- No balance, price or model id written into kit files. Read them live.

## 10. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Silent spend | A generation ran with no spend check shown | The gate before every spend call |
| Blanket yes | One yes reused for later, different jobs | A yes per job |
| Default multiplicity | Four variations charged when one was needed | Set the count |
| Blind retry | Two charges for one image after a timeout | Read the job state |
| Batch first | Twelve images charged before the look was tested | One cheap test, then the batch |
| Flow surprise | A hosted build spends far more than expected | Ask for a total; track against an approved budget |
| Running meter | A rented GPU left running | Stop and confirm |

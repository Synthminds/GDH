# Review on a low-cost preview, and the spend gate for renders

Read this file at steps 15 and 16 of `motion-video`. It covers the preview ladder, what each route offers for a free or cheap preview, the spend gate for generation and render calls, timeouts and job state, and the review checklist.

Evidence. The preview tools named per route (a local preview command, a free scene export and contact sheet, a frame snapshot with a small hourly budget, a quote reference before generation) come from the connector cards, read from schemas and guides on 2026-11-23. No render or generation ran in research, so preview fidelity against the final render is UNTESTED. The spend gate is kernel rule 5.

## 1. The preview ladder

Review at the cheapest level that answers the question. Climb only when the level below passes.

| Level | What it shows | Cost | Answers |
| --- | --- | --- | --- |
| 1. Animatic | Frames on a timeline with sound | Free | Order and pacing |
| 2. Frame check | Key frames rendered as stills or a contact sheet | Free or near free | Composition, type size, safe areas, brand |
| 3. Local or low-resolution preview | The moving piece, unencoded or small | Free on a local route; low on others | Motion, holds, transitions |
| 4. Short paid test | One shot or 5 s at the final settings | Small spend | Generated footage quality; render settings |
| 5. Final render | The full piece | Full spend | Delivery |

Rules:

1. Never send a full paid render as the first look at the motion.
2. For generated footage, approve a still before animating it. A still costs much less than a clip.
3. Test one shot at the final model and settings before generating a batch of shots.
4. Each level gets its own round: shown, question, answers, decision.

## 2. Previews by route

| Route | Free or cheap preview | Card |
| --- | --- | --- |
| Local HTML composer | A local preview server; frame-by-frame scrubbing in the browser; a local render is free | [hyperframes](../../../references/tools/hyperframes.md) |
| Hosted HTML composer | The hosted player shows the project after compose; but compose itself renders and spends | [hyperframes](../../../references/tools/hyperframes.md) |
| Scene engine | Validate, then a contact sheet of exact frames, then a free export | [picsart](../../../references/tools/picsart.md) |
| Remotion blocks | A frame snapshot within a small hourly budget; the hosted editor | [21st-dev](../../../references/tools/21st-dev.md) |
| Video generator | A still first; a quote before each clip; one short clip as a test | [higgsfield](../../../references/tools/higgsfield.md), [elevenlabs](../../../references/tools/elevenlabs.md) |
| Design app video | The app's own preview before export | [canva](../../../references/tools/canva.md), [adobe](../../../references/tools/adobe.md) |

A contact sheet for any local file, with FFmpeg (one frame per second, in a grid):

```
ffmpeg -i preview.mp4 -vf "fps=1,scale=270:-1,tile=6x5" -frames:v 1 contact-sheet.png
```

A low-resolution preview render of a local composition, then check it:

```
ffmpeg -i master-draft.mp4 -vf scale=540:-2 -c:v libx264 -crf 30 -an preview-540.mp4
```

## 3. The spend gate for video

Generation, compose, render, upscale, voice, music and some analysis calls spend. Run the gate for each call or batch.

1. Read the balance from the tool. When the tool cannot report it, ask the user to confirm the balance in their account.
2. Get a quote for the exact job: model, length, resolution, count. Use the tool's quote or estimate call when it has one.
3. Show the user: what will run, how many outputs, the quoted cost, the balance, and the running total against the project's spend limit.
4. Get a yes for this call.
5. Call once. Pass the quote reference or request key when the tool supports one, so the run matches the quote.
6. Keep the job id.
7. Poll at the interval the card gives. Never faster.
8. Download each result at once. Links expire.
9. Record the actual charge when the tool reports it.

After a timeout or an error:

1. Do not call again.
2. Read the job state with the job id, or list recent jobs.
3. When the job ran, use its result.
4. When the job failed, read the reason. A failed run may not be charged; the card says.
5. Retry only with the user's yes. When the tool uses a request key, a retry with the same key is safe and a new key is a new charge. Read the card.

## 4. Render settings before the paid render

Confirm on the free preview before the final render:

| Setting | Check |
| --- | --- |
| Resolution and ratio | Matches the export list |
| Frame rate | One constant rate through the whole pipeline |
| Length | Matches the approved animatic |
| Fonts | The rendered frames use the brand fonts, not a fallback |
| Audio | The final mix is attached; level checked |
| Captions | Burned in or sidecar, as planned |
| Variables | Names and types match the template, for a variable render |

## 5. The review checklist

Watch the preview full screen, then on a phone, then muted.

Message and structure
- [ ] The hook shows the subject within the first one to three seconds.
- [ ] One message; the call to action is clear and held.
- [ ] The muted version carries the message.

Look and brand
- [ ] Type, color and logo match the frame rules.
- [ ] No default font, no generated text or logo, no invented interface.
- [ ] Generated shots are consistent with each other.

Motion and pacing
- [ ] One focal point per shot.
- [ ] Every line holds long enough to read twice.
- [ ] Text does not move while it is read.
- [ ] Transitions are mostly cuts; one signature transition at most.
- [ ] Pacing varies; cuts land on beats.

Sound
- [ ] The voice is clear over the music on phone speakers.
- [ ] Music license recorded; voice source recorded; consent on record where needed.

Accessibility and delivery
- [ ] Nothing flashes.
- [ ] Captions are accurate, synchronized and inside the safe area.
- [ ] Text contrast meets the floor or text sits on a backing.
- [ ] The first frame works as a thumbnail.

Record each finding with: what, where (scene and time), the criterion, severity. Send the chosen fixes to `refine-round`.

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Render to review | The first look at motion is a paid render | Climb the preview ladder |
| Batch before test | Twelve clips generated before one was checked | One test shot at final settings |
| Blind retry | A timed-out render is sent again | Read the job state first |
| Fast polling | Status called every second | Poll at the card's interval |
| Lost result | A render link opened a week later | Download at once |
| Fallback font in render | The final file shows a system face | Check fonts on a free frame render first |
| Spend drift | Many small calls exceed the limit unnoticed | Keep a running total against the limit |

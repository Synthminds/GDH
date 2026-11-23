# Video plan and script

Read this file at steps 1 to 3 of `motion-video`. It covers the video plan, the hook, script writing, timing the read, beats, and a worked example.

Evidence. The order plan, script, beats, storyboard comes from motion design practice recalled from process articles; it was not re-read in this build. The speaking rate of 130 to 160 words a minute is a rule of thumb. The hook window of one to three seconds comes from short-form video guides found by search. The scene and length bands for HTML video come from the HyperFrames send-to guide, read 2026-11-23. Every number here is a default.

## 1. The video plan

Write `video/plan.md` before any other file. It draws on `design/brief.md`, the project brief, and adds what this one video needs. It does not replace the brief. Propose each part the user did not state and get it confirmed.

| Field | Question | Example |
| --- | --- | --- |
| Message | What one thing must a viewer remember? | "Reports that took a day now take ten minutes." |
| Audience | Who watches, and what do they already know? | Operations leads who run weekly reports |
| Placement | Where does it play, and how? | Vertical feed, sound off by default; landing page hero, muted loop |
| Length | Target and maximum | 30 s target, 45 s maximum |
| Ratios | Which frames | 9:16 master, 16:9 and 1:1 versions |
| Call to action | What should the viewer do next? | "Start a free trial" with the URL on the end card |
| Proof | Which real facts, numbers and quotes may appear? | Only the two numbers the user supplied |
| Brand | Tokens, logo files, type, voice rules | `DESIGN.md`, `design/tokens.json`, `design/assets/logo/` |
| Sound | Voice, music, effects, or none | Voice-over plus a light music bed |
| Assets | Real footage, screens, photos, product files | Three product screen recordings |
| Spend limit | Most to spend, in the tool's units | Set by the user |
| Deadline | When, and for which first platform | |

Rules:

1. One message. Two messages make two videos.
2. Proof comes from the user. Invent no statistic, testimonial or customer. Use a labelled placeholder until the real fact arrives.
3. Placement decides sound. A feed video works with sound off. A presentation video may lean on voice.
4. The length follows the message and the placement, not a template.

## 2. Length bands

| Kind | Default length | Default scenes |
| --- | --- | --- |
| Social short, vertical | 10 to 15 s | 5 to 7 |
| Teaser | 8 to 25 s | 4 to 8 |
| Logo sting | 2 s or less | 1 |
| Explainer | 30 to 60 s | 8 to 14 |
| Product walkthrough | 60 to 120 s | One per task step |
| Cinematic title | 45 to 90 s | |

Default: the social, teaser, explainer and title bands are the HyperFrames guide's own bands for HTML video. Confirm the platform's current length limit before you plan a long piece.

## 3. The hook

The first one to three seconds show the subject and a reason to keep watching.

Hook patterns that work without sound:

| Pattern | First frame |
| --- | --- |
| The result first | The finished report on screen, then "How?" |
| The problem, named | "Still building reports by hand?" over the messy spreadsheet |
| The number | The one real number, large, with its unit |
| The motion | The product doing its one striking thing |

Rules:

1. No slow logo intro. The logo belongs at the end, or small in a corner.
2. The first frame works as a thumbnail.
3. The hook uses the brand's look from frame one. A generic opener followed by the brand reads as an ad template.

## 4. Writing the script

Write two columns: what is heard, and what is seen. Keep them in one table.

1. Write the message as the last line first. Then write backwards to the hook.
2. Write for the ear. Short sentences. One idea per sentence. Numbers as they are spoken.
3. Give each sentence one visual. A sentence with no visual is a candidate for cutting.
4. On-screen text is not the voice-over repeated. It names the key word or number only.
5. Write the muted version: the on-screen text alone must carry the message.
6. Mark pauses. A pause before the key number gives it weight.

## 5. Timing the read

1. Read the script aloud at the speed of the intended voice. Time it with a stopwatch.
2. Default: voice-over runs at 130 to 160 words a minute. A 30 s video holds about 65 to 80 words.
3. Leave room: the hook, the end card and transitions take time with no words. Default: plan 20 to 25% of the length without speech.
4. Cut words, not breathing room. When the read runs long, cut a whole beat.
5. Record the timed read, even a rough one. It becomes the guide track for the animatic.

Word budget at 140 words a minute with 20% silence:

| Length | Words |
| --- | --- |
| 15 s | about 28 |
| 30 s | about 56 |
| 45 s | about 84 |
| 60 s | about 112 |

## 6. Beats

Break the script into beats. A beat is one idea, one visual, one line of on-screen text at most.

| # | Time | Heard | Seen | On screen |
| --- | --- | --- | --- | --- |
| 1 | 0.0 to 2.0 | (silence) | The finished report assembles | "10 minutes" |
| 2 | 2.0 to 6.0 | "Weekly reports used to take a day." | A crowded spreadsheet, scrolling | "Was: 1 day" |

Rules:

1. Default: a scene lasts 5 s or less unless the shot needs more. More than about 35 words on one scene: split it. Source: HyperFrames guide defaults.
2. Each beat has one focal point.
3. Each beat states its transition in and out.
4. The last beat is the call to action and the logo, held long enough to read twice.

## 7. Worked example: a 30 s vertical teaser

Plan: message "Weekly reports in ten minutes"; audience operations leads; feed, sound off; 9:16; call to action "Start free".

| # | Time | Heard | Seen | On screen |
| --- | --- | --- | --- | --- |
| 1 | 0 to 2 | music hit | A finished report snaps together from fragments | "10 min" |
| 2 | 2 to 6 | "Your weekly report still takes a day." | A spreadsheet with forty tabs | "Still 1 day?" |
| 3 | 6 to 11 | "Connect your sources once." | Three source logos supplied by the user connect to one node | "Connect once" |
| 4 | 11 to 17 | "Pick the metrics that matter." | Three cards selected on a real product screen | "Pick metrics" |
| 5 | 17 to 23 | "The report writes itself, every Monday." | A calendar flips to Monday; the report appears | "Every Monday" |
| 6 | 23 to 27 | "Ten minutes, not a day." | The two numbers side by side | "1 day to 10 min" |
| 7 | 27 to 30 | (music out) | Logo lockup and URL | "Start free" |

Word count: 27 spoken words in about 20 s of speech. The muted read works from the on-screen column alone.

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Two messages | The script sells a feature and a price change | One message per video |
| Logo first | Four seconds of logo animation before content | Hook first; logo at the end |
| Over-written | 120 words in 30 s | Time the read; cut whole beats |
| Voice repeated on screen | Subtitles of every word as design text | Key word only on screen; captions are separate |
| Silent fails | The video means nothing muted | Write the muted version |
| Invented proof | "Trusted by 10,000 teams" with no source | A labelled placeholder until the user supplies a fact |
| Template order | Logo, problem, three features, testimonial, CTA by habit | Order beats by the message |

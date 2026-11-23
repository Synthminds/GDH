# Sound and voice

Read this file at steps 8, 9 and 17 of `motion-video`. It covers the sound plan, voice-over, designed and cloned voices, music, sound effects, the mix, loudness, captions from a transcript, and consent and licensing.

Evidence. The tool behaviors (voice ids only from a live list, takes and variations multiply cost, a composition node mixes voice and music with ducking, word-timed transcripts for captions) come from the audio connector cards, read from schemas and guides on 2026-11-23. No audio was generated. The loudness and sample-rate targets are from memory and rules of thumb, and are defaults. Capability: `audio`.

## 1. The sound plan

Decide the sound in the video plan, before the storyboard.

| Layer | Question | Default |
| --- | --- | --- |
| Voice | Is there narration? Whose voice? | Voice-over when the message needs words beyond on-screen text |
| Music | What tempo and mood? Licensed or generated? | A bed under the voice, lower in level |
| Effects | Which motions get a sound? | A few, on key motion only: the hook, the reveal, the end card |
| Muted version | Does it work with no sound? | Always yes; captions and on-screen text carry it |

Rules:

1. Plan the muted version first for any feed placement. Many viewers never turn sound on.
2. Music tempo sets the cut rhythm. Pick or specify the music before the animatic.
3. One sound idea per motion. Do not score every element.

## 2. Voice-over

1. Write the script for the ear: short sentences, numbers as spoken, names spelled for pronunciation.
2. Choose the voice from the tool's live voice list. Never use a voice id from memory or from another tool; ids are not shared across tools.
3. Pick by language, accent, age, tone and pace. Match the brand words: calm, sharp, warm.
4. Record or generate one paragraph first. Review it before the whole script.
5. Default: generate one take per line unless the user asks for alternatives. Some tools default to several takes per call; set the count explicitly, because each take spends.
6. Mark pauses and emphasis in the script with the tool's own markup when it has one. Read the card.
7. Check pronunciation of product names, people's names and numbers. Fix with phonetic spelling or a pronunciation rule.
8. Keep the final read file as a separate stem, not only mixed.

### Designed and cloned voices

| Kind | What it is | Gate |
| --- | --- | --- |
| Library voice | A stock voice the tool offers | The tool's terms allow the use |
| Designed voice | A new voice made from a text description | The tool's terms; the preview line comes from the user |
| Cloned voice | A copy of a real person's voice from samples | That person's written consent on record, and the tool's terms |

GATE: no clone of a real person's voice without that person's written consent on record. No imitation of a public figure, an actor or a living artist, with or without a clone. When consent is missing, use a library or designed voice.

Record consent as a consent entry in `design/decisions.md`. Use the fixed entry format of the project template, with a scope that starts `consent,`. Put scope, tool, terms and revocation under `Keep / Change / Remove`. Put where the signed document lives under `Open`, never the document itself. The shape and an example are in `generate-media`, rights reference, section 2. A revocation is a new entry with `Decision: consent revoked (by <who>)`.

## 3. Music

| Route | Use when | Check |
| --- | --- | --- |
| Licensed track from a music library | The brand wants a known feel and has a budget | License covers the platform, the length and paid promotion |
| Free library track | Low budget, short piece | Read the item's license; some free tracks are non-commercial |
| Generated music | A custom bed of exact length | The tool's terms allow commercial use; record it as generated |
| Platform library music inside a social app | Posting natively only | It may not be licensed outside that app |

Rules:

1. Read the music license before the music enters the animatic. A track swapped late changes the pacing.
2. Instrumental under voice. Vocals fight the narration.
3. Cut to length on a musical phrase, not mid-bar. Specify a generated track with the exact length and a clear ending.
4. Record the track in the manifest: source, license, terms read date, and the platforms it covers.

## 4. Sound effects

1. Put effects on key motion only: a hit on the hook, a whoosh on one transition, a click on a product action.
2. Keep each effect short. Default: under one second for interface-like sounds.
3. Match the brand's character. A calm brand gets soft, low effects or none.
4. Use one family of sounds across the piece.

## 5. The mix

1. The voice is always clear. Music sits well below it.
2. Duck the music under speech: lower it while the voice speaks, raise it in gaps. A composition tool may do this automatically. Read the card.
3. Pan nothing important hard to one side. Phones play mono speakers.
4. Leave a short tail of music after the last word, then end on a clean cut or fade.
5. Listen on phone speakers, cheap earbuds and good headphones.

Defaults, from memory and rules of thumb; confirm against each platform's own page:

| Target | Default |
| --- | --- |
| Sample rate | 48 kHz |
| Integrated loudness for online platforms | about -14 LUFS |
| True peak | -1 dBTP or lower |
| Music under voice | well below the voice; judge by ear with the voice level fixed |

Measure loudness with a loudness meter (for example the `ebur128` filter in FFmpeg). Label the result UNTESTED when it was not measured.

```
ffmpeg -i master.mp4 -af ebur128 -f null -
```

## 6. Captions from the transcript

1. Transcribe the final voice with a word-timed transcription tool, or write captions from the script and time them by hand.
2. Correct the transcript against the script: names, numbers, product terms.
3. Split into caption lines of one or two lines each. Default: about 32 to 42 characters a line. Rule of thumb from broadcast practice; check the platform.
4. Each caption stays on screen long enough to read. Default: at least about one second, and no faster than the speech.
5. Export sidecar files (`.vtt` for the web, `.srt` for most platforms) and, when the platform shows no captions, burn them into a version.
6. Place burned captions inside the safe area, clear of the platform's interface.
7. Keep a plain-text transcript beside the video for people who cannot watch it.

## 7. Spend and exposure for audio calls

1. Speech, music, effects, voice design, cloning, transcription and mixing in a hosted tool can each spend. Read the card.
2. Quote first with the tool's estimate mode when it has one. Show the quote, the balance and the number of takes. Get a yes. Call once.
3. A generation call that times out may still run. Read the job state. Never repeat the call blind.
4. Uploading a person's voice sample or a client recording is exposure. Ask first. Name the tool and what it keeps.

## 8. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Voice id from memory | A call fails or picks a different voice | Read the live voice list every session |
| Takes multiply cost | Four takes per line by default | Set the count to one; ask before alternatives |
| Music fights voice | Lyrics under narration | Instrumental bed, ducked under speech |
| Late music swap | Pacing breaks after the license check fails | License before the animatic |
| Clone without consent | A founder's voice cloned from a podcast | Written consent first, or a library voice |
| Sound-only meaning | The joke or the number is only heard | On-screen text and captions carry it |
| Loud master | Clipping or pumping on phones | Measure loudness; keep a true-peak margin |

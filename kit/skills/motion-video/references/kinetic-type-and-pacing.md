# Kinetic type, pacing and holds

Read this file at steps 10 and 14 of `motion-video`. It covers reading time and holds, kinetic type rules, type sizes in the frame, shot length and rhythm, transitions, and the animation principles that apply to video.

Evidence. The hold rule (long enough to read twice) and one focal point per shot come from motion graphics practice summarized in the GDH research; they are rules of thumb. The scene ceiling, the word split, the entrance timing, the minimum type sizes for HTML video and the transition guidance come from the HyperFrames send-to guide, read 2026-11-23; they are that tool's documented defaults, not universal rules. The animation principles come from the Animation Handbook, chapter 2. Every number is a default.

## 1. Reading time and holds

A line of on-screen text holds long enough to be read twice at a normal pace.

Default reading budget, rule of thumb:

| Words on screen | Hold after the text is fully in |
| --- | --- |
| 1 to 3 | about 1.0 to 1.5 s |
| 4 to 7 | about 2.0 to 2.5 s |
| 8 to 12 | about 3.0 to 4.0 s |
| More than 12 | Split into two beats |

Rules:

1. The hold starts when the last word has finished entering. Entrance time does not count as reading time.
2. A number with its unit counts as two words.
3. Captions and design text on screen at the same time compete. Give the design text the shorter wording.
4. The end card holds longest: the call to action and the logo, read twice, plus a beat.
5. Test the holds muted, at full speed, on a phone. If you have to pause to read it, the hold is too short.

## 2. Kinetic type rules

1. Text moves less than the eye can follow. Motion that carries the words in is short; the words then rest.
2. One text animation pattern per piece, plus one accent. A different effect on every line reads as a template.
3. Animate by line or by word for headlines. Animate by character only for short display words and only when the brand is playful.
4. Keep the reading order. Words enter in the order they are read.
5. Do not move text while it is being read. Ambient drift on text, if any, is slower than reading would notice.
6. Exit text before the next line enters, or cut. Two lines competing for attention fail both.
7. Emphasis comes from timing and scale, not from a second typeface or a gradient fill.
8. Use the brand's display face for headlines and its text face for small text. Do not add faces for video.

Patterns, with when to use them:

| Pattern | Use for | Avoid when |
| --- | --- | --- |
| Line rise (short travel plus fade) | Most headlines | Every single line in the piece |
| Word stagger | A key sentence with rhythm | Long sentences |
| Mask reveal | A bold single word or number | Small text |
| Counter roll | A real number rising to its value | Invented numbers |
| Highlight sweep | One key word in a sentence | More than once per scene |
| Type on beat | Music-led edits | Voice-led edits; words would fight the voice |

## 3. Type sizes in the frame

Default minimums for HTML video at 1080 px on the short side, from the HyperFrames guide: headlines 60 px, body 20 px, labels 16 px. Treat them as floors for that tool's compositions; test on a phone for every route.

Rules:

1. Size for the phone. A 1080 by 1920 frame shown at about 390 px wide is scaled to roughly a third.
2. Text over footage needs a backing or a scrim when contrast against the busiest frame is uncertain.
3. Keep text inside the safe area for the platform. See `export-and-delivery.md`.
4. Captions are sized for reading. Default: caption text height about 4 to 5% of the frame height. Rule of thumb.

## 4. Shot length and rhythm

1. One idea and one focal point per shot.
2. Default: a scene lasts 5 s or less unless the shot needs more (HyperFrames guide default).
3. Vary shot length. Equal lengths read as a slideshow. Alternate a quick beat with a held beat.
4. Cut on the beat of the music, or on the stress of the voice line.
5. Put the first motion of each scene shortly after the cut. Default: the first entrance starts 0.1 to 0.3 s into the scene (HyperFrames guide).
6. Keep something alive in a held shot: a slow push, a drift, a light sweep. A dead frame feels like a freeze. Keep that motion slower than reading.
7. Plan the energy curve: hook (high), problem (medium), proof (rising), resolution (calm), call to action (clear and held).

Energy curve for a 30 s teaser:

| Time | Beat | Energy | Cut rate |
| --- | --- | --- | --- |
| 0 to 2 | Hook | High | One hard cut in |
| 2 to 6 | Problem | Medium | Held |
| 6 to 17 | Steps | Rising | One cut per step |
| 17 to 23 | Payoff | Peak | Quick |
| 23 to 27 | Proof number | Calm | Held |
| 27 to 30 | Call to action | Clear | Held to the end |

## 5. Transitions

1. Mostly hard cuts. A cut is the clearest transition.
2. Default: one signature transition style at most in a piece, used at the key moments. The HyperFrames guide advises at most one contiguous shader chain in a first draft.
3. A match cut (shape or motion continues across the cut) connects two ideas. Use it for the turn of the story.
4. A transition has a duration. Default minimum 0.3 s; about 0.5 s reads as smooth (HyperFrames guide, for its shader transitions).
5. Never transition and introduce new text at the same moment.

## 6. Animation principles in video

| Principle | In a motion graphic |
| --- | --- |
| Timing and pacing | Duration matches size, distance and importance |
| Slow in, slow out | Ease every move through space; linear only for constant motion |
| Anticipation | A small counter-move before a big move |
| Follow-through | A slight overshoot and settle on a prominent move, if the brand allows |
| Overlapping action | Related elements offset in time, not all on one frame |
| Secondary action | Supports the main move, never steals attention |
| Staging | One thing to look at; the frame leads the eye to it |
| Appeal | A signature move the brand can own, used at key moments only |

Video allows longer, more expressive motion than an interface, because the viewer is not waiting to act. The brand's motion character still holds. A brand with no springs gets no bouncy type in its video.

## 7. Easing in video

1. Ease-out for arrivals, ease-in for departures off frame, ease-in-out for moves within the frame.
2. Vary eases within a scene so motion does not look machine-made. The HyperFrames guide asks for at least two motion patterns and three eases per scene. Treat that as that tool's default.
3. Read the brand's motion curve from the tokens and use it for the signature moves.

## 8. Worked example: one beat, timed

Beat 5 of the teaser: "The report writes itself, every Monday." On screen: "Every Monday". 6 s.

| Time in scene | Event |
| --- | --- |
| 0.0 | Cut in on the music downbeat. Calendar card on screen, slow push in starts. |
| 0.2 to 0.6 | Calendar page flips to Monday (ease-in-out). |
| 0.8 to 1.2 | "Every Monday" rises 24 px with a fade (brand ease-out). |
| 1.2 to 3.4 | Hold for reading: two words, about 2 s. |
| 1.6 to 3.6 | The report fills in line by line behind the text, at low contrast. |
| 3.6 to 5.6 | The report sharpens; the text exits first, at 3.6 to 3.8. |
| 6.0 | Hard cut to beat 6. |

## 9. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Unreadable text | Viewers pause to read | Hold for two reads; split long lines |
| Effect salad | Every line uses a different text effect | One pattern plus one accent |
| Moving while reading | Text drifts or scales during its hold | Words rest once in |
| Slideshow rhythm | Every shot is exactly 3 s | Vary shot length; cut on beats |
| Transition parade | A shader between every scene | Hard cuts; one signature transition |
| Tiny type | Labels illegible on a phone | Size for a scaled phone frame; test on a phone |
| Everything at once | All elements enter on one frame | Overlap and offset; one focal point |

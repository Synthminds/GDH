# Design persona

A user persona says who the audience is. A design persona says who the product is. It keeps the look, the words and the behavior in one character when many hands work on them.

The form below is GDH's own rewrite of the eight-field persona that Designing for Emotion describes in chapter 3. `align` asks one field at a time, with questions 5.1 to 5.9 of its question bank. This skill fills the form from the answers, runs the checks and saves the result in section 6 of `design/brief.md`.

## Which form to run

| Form | Fields | Use for |
| --- | --- | --- |
| Full | 1 to 8 | A brand, a logo, a design system, a new site or a new app |
| Short | 2, 4 (three traits) and 5 | Product and page size: a dashboard, a chart, an infographic, a video, a 3D piece, any refine job |
| Read back | none | Asset size, or `DESIGN.md` already holds a voice and traits. Read them back and ask "Still true?" |

The job size that `align` names sets the default form. The full form serves brand size: a brand, a logo, a design system, a new site or a new app.

## How to fill it

1. Read the inputs: the people in section 2, the competitors in section 8, any brand guide, any mascot or logo.
2. Copy the opening answer ("If this product were a person in the room, who would it be?") word for word.
3. Fill one field for each answer in the record. A field the user skipped holds your proposal, marked ASSUMED.
4. Tie the three brand words to the traits. Each brand word becomes one of the first three traits.
5. Run the checks. Then run the contrast test. A failed check goes back to `align` as one question.

## The form

```
DESIGN PERSONA

1. Name
   Product, brand or service: ______

2. Character
   Who it is, as a person, in two to four sentences: ______
   What makes it unlike others in its category: ______

3. Stand-in
   A person, character or mascot that carries the character: ______
   Kind: real public figure | someone the team knows | invented character | existing mascot
   Why this one, in one line: ______
   Use: internal reference only, unless rights are cleared.

4. Traits (five to seven; the first three are the brand words)
   1. ______, but not ______
   2. ______, but not ______
   3. ______, but not ______
   4. ______, but not ______
   5. ______, but not ______
   6. (optional) ______, but not ______
   7. (optional) ______, but not ______
   Never: ______

5. Voice
   How it speaks, in one or two sentences: ______
   Habits (contractions, sentence length, humor, case): ______
   How the voice shifts:
     when the user succeeds: ______
     when the user makes an error: ______
     when the product fails: ______
     when the user is anxious or in a hurry: ______

6. Real strings (write the exact words)
   Success: "______"
   User error: "______"
   Product failure: "______"
   Empty or first-run state: "______"

7. Visual lexicon (each line ends with a trait)
   Color: ______ because ______
   Type: ______ because ______
   Style (shape, texture, imagery, illustration, motion): ______ because ______
   Character or mascot rules (where it may and may not appear): ______

8. Moments
   Peak 1: at step ______ the user feels ______; we respond with ______
   Peak 2: at step ______ the user feels ______; we respond with ______
   Low point: at step ______ the user feels ______; we respond with ______
```

Field 7 states intent in words. It names no hex value and no font file. `mood-board` proposes those.

## Checks

Run each check before you show the persona.

| # | Check | Pass when |
| --- | --- | --- |
| 1 | Trait count | Five to seven traits on the full form; three on the short form |
| 2 | Limits | Every trait has a "but not" limit that names a real risk of that trait |
| 3 | Never | One trait to avoid is named |
| 4 | Brand words | The three brand words are traits 1 to 3 |
| 5 | Voice shifts | Four situations are filled. Humor falls and plainness rises as the situation gets worse |
| 6 | Real strings | Three or more exact strings exist: success, user error, product failure |
| 7 | Because | Every visual lexicon line ends with a trait from field 4 |
| 8 | Moments | One peak and one low point are filled on the full form |
| 9 | Work path | A mascot or character never appears in an error, a data readout, validation or task instructions |
| 10 | Contrast | The persona fails the contrast test below for both named competitors |

A "but not" limit must cut. "Friendly, but not unfriendly" fails. "Friendly, but not chatty" passes: it tells a writer where to stop.

## The contrast test

1. Put the Character and Traits fields beside two competitors the user named.
2. Ask the user: "Could this describe either of them?"
3. When the answer is yes, return to fields 2 and 4. Sharpen until the answer is no.
4. Then ask: "Who will this put off?" A clear character repels some people. Record them under "Not for" in section 2 of the brief.

A review comment such as "this may not appeal to everyone" is not a reason to flatten the persona. The "Not for" line already accepts it.

## The dose test

Personality serves the task. Test each real string:

1. Delete the personality words.
2. When the message gets clearer, or the user reaches the action sooner, keep the shorter version.
3. No joke comes before the information the user needs.

## Worked example

This example is invented for illustration. The product does not exist.

```
1. Name: Tidewatch, a tide and weather app for small-boat sailors.

2. Character
   An experienced harbor master who has seen every mistake and judges none of them.
   Says little, says it early, and is right. You trust the short answer.
   Unlike the category: other marine apps show every instrument at once.
   Tidewatch tells you the one thing that matters for the next two hours.

3. Stand-in: an invented character, "the harbor master on the radio".
   Why: a calm voice you hear before you see the water.

4. Traits
   1. Calm, but not sleepy
   2. Exact, but not technical
   3. Weathered, but not nostalgic
   4. Direct, but not curt
   5. Watchful, but not alarmist
   Never: playful

5. Voice
   Short declarative sentences. Numbers first, then the meaning.
   Habits: no exclamation marks, no humor, units always shown.
   Success: one plain line of confirmation.
   User error: says what to change, with the value that works.
   Product failure: says what is unknown and since when.
   User in a hurry: the single number, large, and nothing else.

6. Real strings
   Success: "Route saved. High water at 14:20."
   User error: "Draft must be between 0.3 and 4 m. You entered 40."
   Product failure: "No tide data since 09:15. Showing the last forecast."
   Empty state: "Add your home harbor to see today's window."

7. Visual lexicon
   Color: wet slate, and the green and red of navigation lights for go and stop, because exact.
   Type: a sturdy grotesque with tabular figures, because exact.
   Style: matte surfaces, chart-paper hairlines, no gloss, because weathered.
   Character rules: no mascot. The harbor master is a voice, never a picture.

8. Moments
   Peak 1: at "check before leaving" the user feels unsure; we respond with one go or no-go line.
   Peak 2: at "back in harbor" the user feels relief; we respond with a quiet log entry.
   Low point: at "data is stale" the user feels exposed; we respond with the age of the data, first.
```

Why this persona works:

- Each limit names the failure of its own trait. "Watchful, but not alarmist" stops red banners for mild wind.
- The strings carry numbers and units. A builder can copy them into the product.
- The lexicon gives reasons a reviewer can test. "Navigation green because exact" fails when green decorates a headline instead of marking the safe action.
- It fails the contrast test for an instrument-heavy competitor. That is the point.

## Persona failure patterns

| Pattern | Sign | Correction |
| --- | --- | --- |
| Adjective list | Seven traits, no limits | Add "but not" to each, or cut the trait |
| Everyone's persona | "Friendly, modern, trustworthy" | Run the contrast test. Replace each word a competitor could claim |
| Voice without strings | A paragraph on tone, no real message | Write the four strings |
| One tone for all weather | The failure message jokes | Rewrite by severity |
| Lexicon as spec | "Color: #1E2A38" in field 7 | Write the intent and the trait. Values come from the direction |
| Mascot in the way | A character delivers error text | Remove it from the work path |
| Borrowed face | A real celebrity is the stand-in and appears in a board | Keep it internal. A likeness never ships without rights |

# Designing for Emotion, second edition (A Book Apart)

Book id `designing-for-emotion`, id prefix `P-EMO`. 37 principles, 11 of them gates. The machine-readable copy is in [principles.json](../principles.json); this file matches it word for word.

Gates: P-EMO-01, P-EMO-02, P-EMO-03, P-EMO-06, P-EMO-07, P-EMO-11, P-EMO-20, P-EMO-21, P-EMO-27, P-EMO-33, P-EMO-35.
Every other principle is a default. Query them with the `design-principles` skill.

## Chapter 1: Emotional design

**P-EMO-01 Climb the four needs in order.** Check every core task for function, reliability and usability before adding pleasure, and block pleasure work on any task that fails the first three. Test: Each core task has a pass for function, reliability and usability before any pleasure element is added to it.

**P-EMO-02 Go past usable on purpose.** Give every deliverable at least one deliberate element whose job is emotional, and name the feeling it targets. Test: The design notes name at least one emotional element per deliverable and its target feeling.

**P-EMO-03 Cut delight that blocks tasks.** Remove or move any emotional element that adds a step, covers a control, delays feedback or hides a status. Test: No emotional element adds a step, hides a control or delays feedback.

**P-EMO-04 Find the ownable moments.** List the steps where the user's emotion changes sharply, up or down, with the expected emotion and the planned response for each. Test: A list of ownable moments exists with step, emotion, direction and response for each.

**P-EMO-05 Meet the emotion of the moment.** Change copy and behavior at each ownable moment to match the user's state, such as a plain condolence at a loss or a real celebration after a long task. Test: At each ownable moment the text or behavior differs from the default pattern and fits the expected emotion.

**P-EMO-06 Pleasure only where needs meet.** Tie every reward, streak or notification to a benefit for the user, and remove any whose only beneficiary is the business. Test: Each reward, streak and notification has a written user benefit.

**P-EMO-07 Do not ship framework defaults.** Never call a look finished while its type or its color is the unmodified default of the framework or library used. Test: Type and color each differ from the library default, or the design system prescribes the default.

## Chapter 2: Design for humans

**P-EMO-08 Contrast marks what matters.** Use strong contrast only on the few elements that matter most, and give every high-contrast element a stated priority. Test: The first elements a viewer names match the intended priority order.

**P-EMO-09 One loud element per view.** Let only one element per view carry the primary visual weight, and demote any rival that competes with it. Test: A reviewer can name the single primary action of each view.

**P-EMO-10 Remove choices before adding.** Count navigation items, calls to action and promotional blocks per view, and justify any increase with a user task. Test: Any increase in choices per view carries a written reason tied to a user task.

**P-EMO-11 Simulate color vision deficiency.** Run status and category colors through a color vision deficiency simulation and keep every pair distinguishable. Test: Status and category pairs stay distinguishable in a color vision deficiency simulation.

**P-EMO-12 Notify only for user action.** Send a notification, badge or alert only when the user needs to act on it, and keep promotional interruptions off by default. Test: Every notification type has a user-side trigger and action, and none is promotional by default.

**P-EMO-13 Aesthetics is part of usability.** Run a separate aesthetic pass with named criteria such as proportion, type, color, spacing and finish, and never defer it as decoration. Test: The review contains an aesthetic pass with named criteria.

**P-EMO-14 Break the category's norms.** Place the concept beside several competitors and name at least two category conventions it breaks on purpose, within what the design system allows. Test: The notes name two or more deliberately broken category conventions, and a reviewer can pick the concept out of the lineup.

**P-EMO-15 Faces and rounded forms for warmth.** When the brief asks for warmth or approachability, bring a human presence into the concept, such as a face, character or soft rounded form, checked against the persona. Test: An approachable brief's concept includes a human or face-like element that the persona supports.

## Chapter 3: Personality

**P-EMO-16 Write a design persona.** Write a design persona before visual or copy work: overview, a reference figure, traits, voice, copy samples, a visual lexicon and engagement methods. Test: A design persona file exists with every field filled.

**P-EMO-17 Traits with limits.** Give the persona a handful of traits, each paired with the edge it must not cross, plus one trait to avoid entirely. Test: Every persona trait has a but-not limit and one avoided trait is named.

**P-EMO-18 Lexicon gives each choice a trait.** Give every palette, typeface and style rule in DESIGN.md a because clause that names the persona trait it expresses. Test: Each palette, type and style rule in the visual lexicon has a because clause naming a trait.

**P-EMO-19 Personality in look, words and behavior.** Express the personality through visual design, copy and interaction together on every key screen. Test: Each sampled key screen shows a named trait in all three channels.

**P-EMO-20 Tone drops humor as stakes rise.** Write copy samples for success, user error and critical failure, and remove humor as severity rises. Test: Side by side, the samples show humor falling and plainness rising with severity.

**P-EMO-21 Mascot stays out of the work.** Keep any mascot or character out of errors, data readouts, validation and task instructions. Test: No character appears in error messages, data, form validation or instructions.

**P-EMO-22 Clarity beats cleverness.** Delete the personality words from each message, and ship the shorter version whenever it is clearer or faster. Test: No message gets clearer when its personality words are removed, and no joke precedes needed information.

**P-EMO-23 Metaphor tames intimidating subjects.** For an abstract or feared subject, name the misconception or fear to overcome and choose a character, metaphor or illustration that disarms it. Test: The concept states the fear or misconception it targets and the metaphor chosen for it.

**P-EMO-24 Accept who will dislike it.** Name who the personality is not for, and do not flatten a design only because it might not appeal to everyone. Test: The persona or brief names who the brand is not for.

## Chapter 4: Empathy and inclusion

**P-EMO-25 Intent versus impact per feature.** For each major feature, write the intended effect, the worst plausible misuse or harm, the group that bears it and the mitigation. Test: Each major feature has an intent-versus-impact entry with a mitigation.

**P-EMO-26 All-people statements expose exclusion.** Write each key assumption as a sentence that starts with all people can, then list the groups for whom it is false and the design response. Test: Each key interaction has an all-people statement with failing groups and responses.

**P-EMO-27 Represent varied people by default.** Show varied skin tones, ages, genders, body types and disabilities across human imagery, and build that variety into the system's illustration and avatar parts. Test: Human imagery does not repeat a single default person across all figures.

## Chapter 5: Emotional engagement

**P-EMO-28 Fix valleys, place one peak.** Map the journey's emotional highs and lows, fix each low with usability or speed and no humor, and place the main peak where a key step closes. Test: Each low step's fix is a usability or speed change, and each key flow ends on a designed state.

**P-EMO-29 Surprise rarely, at peaks.** Place surprises only at mapped peaks, never in a low moment, and never so often that they become the pattern. Test: Every surprise sits at a mapped peak and none repeats into a pattern.

**P-EMO-30 Story in three beats.** Shape any piece meant to be remembered or acted on as tension, turning point and resolution. Test: The outline has all three beats; a piece missing one is a list, not a story.

**P-EMO-31 Admit a limit plainly.** State at least one true limitation, open problem or weak result in plain words where the audience is skeptical. Test: The page states at least one real limitation and contains no unsupported claim.

## Chapter 6: Trust, fear, and forgiveness

**P-EMO-32 Answer fears near the top.** List the audience's top fears and answer each near the top of the page in order: the simple fact, the proof, privacy, then technical detail. Test: Each listed fear has an answer near the top in that order.

**P-EMO-33 Plain terms beside the action.** State what happens to data, money and safety in plain language next to the action that commits it. Test: Every consent, payment or data request has a plain-language statement next to the action.

**P-EMO-34 Calm defaults for volatile data.** Choose the default range and first metric of volatile data views to support good long-term decisions, not to look alarming. Test: Each volatile chart records its default range and first metric with a reason.

**P-EMO-35 Failure messages are honest updates.** Make failure and outage messages say what happened, what is safe, what is being done and when the next update comes, with an apology and no jokes. Test: The failure template has the four facts, an apology and no humor.

## Chapter 7: The business of emotional design

**P-EMO-36 Every layer in every slice.** Scope each iteration, including the first release, with at least one item for function, reliability, usability and pleasure. Test: The iteration scope has an item in each of the four layers.

**P-EMO-37 Measure each emotional moment.** Give each designed peak moment a metric and a baseline before launch, and report the change as a number. Test: Each peak moment has a metric with a baseline in the handoff.

Sources: Designing for Emotion, second edition (A Book Apart); Chapter 1: Emotional design, Chapter 2: Design for humans, Chapter 3: Personality, Chapter 4: Empathy and inclusion, Chapter 5: Emotional engagement, Chapter 6: Trust, fear, and forgiveness, Chapter 7: The business of emotional design. Paraphrased in the kit's own words; no sentence is quoted.

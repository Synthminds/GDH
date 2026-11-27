# Animation Handbook (InVision DesignBetter)

Book id `animation-handbook`, id prefix `P-ANI`. 32 principles, 7 of them gates. The machine-readable copy is in [principles.json](../principles.json); this file matches it word for word.

Gates: P-ANI-01, P-ANI-04, P-ANI-05, P-ANI-11, P-ANI-21, P-ANI-26, P-ANI-27.
Every other principle is a default. Query them with the `design-principles` skill.

## Chapter 1: Motion's purpose

**P-ANI-01 Every animation needs a purpose.** Give each animation one stated purpose, such as showing a state change, cause and effect, where something went, attention, feedback, a hidden affordance or brand emotion, and cut any with none. Test: Every row of the motion spec has a purpose from the allowed list.

**P-ANI-02 Animate changes people would miss.** Add an in-between state to any change that would otherwise happen instantly and leave people unsure what changed. Test: Each listed state change has a transition or a recorded reason for none.

**P-ANI-03 Show origin and destination.** When an object enters or leaves because of a user action, move it from where it came from or to where it now lives. Test: After one viewing, a reviewer can name where each entering or leaving element came from or went.

**P-ANI-04 Motion never carries meaning alone.** Give every meaningful visual change a non-visual equivalent, such as an announcement, a state attribute or an accessibility label. Test: The number of meaningful animations equals the number of matching non-visual signals in the code.

**P-ANI-05 Primary actions never hide.** Keep core controls visible at rest and use motion only to hint at secondary features that are tucked away. Test: With motion paused, every primary action of each screen is visible.

**P-ANI-06 Push back at limits.** Make a control that cannot go further respond with gentle resistance and return, instead of doing nothing. Test: No tested limit is a silent dead end.

**P-ANI-07 Match motion to product temperament.** Choose motion character from the brand's emotional tone: springier for playful, fast and tight for precise tools, slow and even for calm. Test: A reviewer who watches the prototype without the brief picks adjectives that overlap the brief's motion adjectives.

**P-ANI-08 Ration expressive motion.** Reserve large expressive animation for a few named moments in the journey, such as finishing a big task, and keep everything else functional. Test: No screen runs more than one expressive animation at once, and each expressive one maps to a named moment.

## Chapter 2: Principles of animation

**P-ANI-09 Perceptible duration for meaning.** Give any transition meant to be seen enough time to register, and allow shorter times only for press feedback. Test: No meaningful transition in the tokens or code is shorter than the stated floor.

**P-ANI-10 Several durations, not one.** Use a small duration scale with different steps for view changes, small state changes and loaders, and lengthen each only as much as it needs. Test: The duration scale has more than one step and each token names its role.

**P-ANI-11 No linear easing on movement.** Never move an object at constant speed; give movement acceleration and deceleration. Test: No transform or position animation uses linear timing except a continuous loop.

**P-ANI-12 Ease out in, ease in out.** Default to decelerating curves for elements that enter or gain attention and accelerating curves for elements that leave or lose it. Test: Each enter animation uses an ease-out token and each exit an ease-in token, or a logged exception.

**P-ANI-13 Name the physical analog.** Choose any non-default easing by naming the real object it imitates, such as a drawer, a door or a sheet of paper. Test: Every non-default easing in the spec names its analog.

**P-ANI-14 Springs barely seen, scoped.** Keep overshoot at the edge of perception and use springs only where the design system allows them, or, with no system, on gesture-driven or interruptible movement. Test: A first-time viewer does not describe any element as bouncing, and no spring is applied to opacity or color.

**P-ANI-15 Stage before swapping in place.** Before replacing content in place, such as a caption or status, add a brief out phase or pause so the viewer notices the change. Test: No in-place content replacement is a hard cut.

**P-ANI-16 Numbers move with their direction.** Animate a changing number upward when it rises and downward when it falls, instead of only flashing it. Test: Raising and then lowering a metric produces two opposite motions and an exact final value.

**P-ANI-17 Secondary motion stays secondary.** Keep supporting motion weaker than the primary motion so it adds nuance without drawing the eye. Test: A first-time viewer names the primary element first when asked what moved.

**P-ANI-18 Stagger groups, cap the total.** Offset the start of similar items entering together, shrink the gap between successive items, and keep the total cascade time capped at any item count. Test: Per-item delay is above zero, the gaps shrink, and the total time stays within the project cap at every tested count.

**P-ANI-19 Choose signature motions.** Define a small set of signature motions that carry the brand and state where each may appear. Test: The motion section names its signature motions with allowed places, and each appears only there.

## Chapter 3: Animation collaboration

**P-ANI-20 Plan motion at wireframe stage.** Write motion notes, meaning what moves, from where and why, into the first layout deliverable instead of adding motion after the build. Test: The first layout deliverable contains motion notes.

**P-ANI-21 Spec motion in four blocks.** Describe every animation with the same four fields: behavior, easing, duration and sequencing. Test: Every row of the motion spec has behavior, easing, duration and sequencing filled.

**P-ANI-22 One environment statement.** State the single feeling every detail must support, such as calm and unhurried, and reject motion that breaks it. Test: The brief holds one environment statement and each motion review records a yes or no against it.

**P-ANI-23 Tune timing in a sandbox.** Tune timing in a standalone prototype with adjustable variables, and ship the exact values signed off there. Test: Production motion values equal the values recorded at prototype sign-off.

**P-ANI-24 Motion is a system section.** Keep motion principles, duration and easing tokens, guidance per interaction type and examples together in one section of the design system. Test: The design system has a motion section with principles, tokens and guidance per interaction type.

**P-ANI-25 Bake motion into components.** Build curves and durations into shared components so feature work never picks timing per instance. Test: Feature code holds no per-instance duration or easing override without a logged exception.

**P-ANI-26 Message stays long enough.** Give every auto-dismissing animated message a minimum display time long enough for a reader and a screen reader to finish it. Test: Each auto-dismissing element has a documented minimum time and is fully read by a screen reader before removal.

**P-ANI-27 Gestures need a labelled alternative.** Give every gesture-only action a focusable, labelled control or an accessibility action that does the same thing. Test: Every gesture-triggered action is reachable through a labelled control.

## Chapter 4: Taking animation further

**P-ANI-28 Reduce until nearly unseen.** Shrink each animation's amplitude, duration and number of moving parts until it stops communicating, then step back one notch. Test: Critique notes record a reduction check for each animation.

**P-ANI-29 Connect states through shared elements.** Animate the content two states share, such as the tapped card growing into its detail view, instead of sliding in an unrelated screen. Test: No list-to-detail transition uses a generic push when shared elements exist.

**P-ANI-30 Test motion in the worst case.** Judge each animation at the largest realistic data volume and in the lowest-attention situation the users face. Test: Each animation has a recorded pass or fail at maximum realistic data and in the lowest-attention scenario.

**P-ANI-31 Look alike, respond alike.** Give elements that look alike the same class of response to the same input, and give a member that cannot act a soft response in the same physical language. Test: Within each visual group the same input produces the same class of response, and no member is inert.

**P-ANI-32 Gestures track and reverse.** Make gesture-driven motion follow the input continuously and let the user reverse or cancel it halfway. Test: Reversing a drag halfway returns the element smoothly with no jump or forced completion.

Sources: Animation Handbook (InVision DesignBetter); Chapter 1: Motion's purpose, Chapter 2: Principles of animation, Chapter 3: Animation collaboration, Chapter 4: Taking animation further. Paraphrased in the kit's own words; no sentence is quoted.

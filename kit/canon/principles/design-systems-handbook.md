# Design Systems Handbook (InVision DesignBetter)

Book id `design-systems-handbook`, id prefix `P-DSH`. 32 principles, 14 of them gates. The machine-readable copy is in [principles.json](../principles.json); this file matches it word for word.

Gates: P-DSH-01, P-DSH-02, P-DSH-04, P-DSH-08, P-DSH-11, P-DSH-12, P-DSH-14, P-DSH-21, P-DSH-22, P-DSH-23, P-DSH-24, P-DSH-25, P-DSH-26, P-DSH-27.
Every other principle is a default. Query them with the `design-principles` skill.

## Chapter 1: Introducing design systems

**P-DSH-01 Pair every standard with purpose.** Write the reason and the intended use next to every token group and component, not only its value. Test: Every token group and component entry in DESIGN.md has a non-empty purpose or use-when line.

**P-DSH-02 Extend the system, not exceptions.** When a screen needs something the system lacks, add it to the system first and then use it, instead of styling a local exception. Test: Every style in the deliverable maps to a system entry or to a logged exception.

**P-DSH-03 Give each component one job.** Describe each component's job in one sentence and split any component whose description needs a second job joined by and. Test: Each component doc states a single job in one sentence.

**P-DSH-04 Version the system as product.** Give the design system a version number, a changelog and a named owner, and treat the first release as version one rather than the finish. Test: DESIGN.md or the token file carries a version, an owner and a changelog entry for its last change.

## Chapter 2: Designing your design system

**P-DSH-05 Inventory before redesigning a product.** Count the unique colors, type sizes, type families and spacing values of an existing product before proposing a system for it. Test: An inventory lists current and target counts per attribute, or the brief states that the product does not exist yet.

**P-DSH-06 Board every variant, then merge.** Collect one screenshot of every live variant of each interface element on a single board and mark each keep, merge or remove. Test: Each element group on the board has a screenshot per variant and a decision per variant.

**P-DSH-07 Ask system users first.** Before designing a system, ask the people who will build with it and the person who funds it what hurts today and how success will be measured. Test: The brief names the people consulted, their problems and one measurable goal for the system.

**P-DSH-08 Give every color one job.** Assign each palette color one role, such as action, feedback, information or hierarchy, and never let one value carry two conflicting roles. Test: Every palette entry has exactly one stated role, and no value serves both a brand role and a status role.

**P-DSH-09 Grow the palette on demand.** Start the palette from a few brand primaries, one interactive color, neutrals and state colors, and add a tint or shade only when a component needs it. Test: Each tint and shade in the palette is used by at least one component.

**P-DSH-10 Shift hue when shading colors.** When darkening or lightening a hue turns it muddy, mix toward a neighboring hue instead of pure black or white. Test: Viewed side by side, no step of a hue ramp reads as a different hue family.

**P-DSH-11 Record contrast for every pairing.** Measure and record the contrast of every text and background pair the palette allows, using the thresholds of the accessibility gate. Test: A contrast grid lists each allowed foreground and background pair with its ratio and a pass or fail mark.

**P-DSH-12 Never code categories by color alone.** Pair every color-coded category or state with a label, icon, pattern or position. Test: Every color-coded category in the deliverable also carries a non-color cue.

**P-DSH-13 Load few families, justify weights.** Use one text family plus a monospace where code appears, add a display face only with a written reason, and list every loaded weight with its purpose. Test: The type spec lists every loaded family and weight with a reason for each.

**P-DSH-14 Thin weights only at display.** Reserve thin and light weights for display sizes and keep any text below heading size at regular weight or heavier. Test: No text style smaller than the smallest heading uses a weight lighter than regular.

**P-DSH-15 Derive sizes from one scale.** Derive every type size from one base size and one ratio, and list any size that falls off that scale. Test: Each size token equals the base times the ratio to an integer power, within rounding, or is listed as an exception.

**P-DSH-16 Unitless leading, tighter for headings.** Set line height as a unitless multiple, looser for body text and tighter for headings. Test: Line-height tokens carry no unit and the body value is larger than every heading value.

**P-DSH-17 Space on a four-based scale.** Take every spacing and sizing value from one scale built on a base of four, and comment any off-scale value with its reason. Test: Every spacing token is a multiple of the base, and each exception in the styles carries a comment.

**P-DSH-18 Let content set the size.** Avoid fixed widths and heights so elements fill their container, and give images a maximum width with automatic height. Test: At phone width and wide desktop width nothing overflows or clips, and each fixed dimension in the styles has a reason.

**P-DSH-19 Write the icon spec first.** Write the icon rules, meaning fill or outline, stroke weight, color count, sizes and live area, before drawing, and ship icons and illustrations as vector. Test: The icon spec answers all five questions and ten sampled icons match it.

**P-DSH-20 Tokenize the material layer.** Give shadows, elevation, radii, borders and textures fixed token values, like color and type. Test: The distinct shadow and radius values in the artifact do not outnumber the tokens defined for them.

## Chapter 3: Building your design system

**P-DSH-21 Store every value as token.** Keep every reusable color, size, space, radius and duration as a named token in one platform-neutral file, and reference only tokens in component styles. Test: A scan of component styles finds no raw color, size or duration literal that a token covers.

**P-DSH-22 Theme by swapping values only.** Build themes and sub-brands by changing token values over identical structure and markup. Test: Two themes differ only in token values; markup, class names and scripts are identical.

**P-DSH-23 Show every state as fixtures.** Show each interactive component in every state it can take, including hover, focus, active, disabled and error, and reuse those examples as test fixtures. Test: For each interactive component the docs show every applicable state and the tests load those same examples.

**P-DSH-24 Build accessibility into components.** Make each component keyboard operable, labelled and usable by a screen reader inside the system so every product inherits it. Test: Each component example works by keyboard alone and passes an automated accessibility check with zero errors.

**P-DSH-25 Breaking changes bump major.** Version releases as major.minor.patch and bump the major number for any removed or renamed token, class or property. Test: Every release that removes or renames a token, class or property carries a major bump and notes.

**P-DSH-26 Deprecate with a path, never clone.** Never fork a component under a new name to dodge a breaking change; deprecate it with a replacement, a migration note and a removal date. Test: No component name carries a numeric or new/old suffix, and each deprecated item has a replacement, a note and a date.

## Chapter 4: Putting your design system into practice

**P-DSH-27 Undocumented means outside the system.** Treat any pattern missing from the documentation as outside the system, and keep the list of components in code identical to the list in the docs. Test: A diff of component names in code against component names in the docs is empty.

**P-DSH-28 Keep a candidates waiting room.** Hold patterns that recur but are not yet in the system in a visible candidates list with where each is used and the decision pending. Test: Each candidate lists where it is used and a pending decision.

**P-DSH-29 Pilot on one real feature.** Prove a new system on one real, self-contained feature, then review the system for bias toward that feature before generalizing it. Test: The decision record names the pilot or the first incremental piece and a bias review after it.

## Chapter 5: Expanding your design system

**P-DSH-30 Write a ranked priority line.** Write one line that ranks the project's top qualities in order, such as clarity before elegance, so trade-offs resolve the same way every time. Test: The brief holds a ranked priority line and later decisions that trade qualities cite it.

**P-DSH-31 Define voice by is and never.** Define the writing voice with a few words for what it is now, what it aims to be and what it never is, and turn those words into per-channel copy rules. Test: The voice section lists is, aims-to-be and never words, and each channel has at least one concrete rule derived from them.

## Chapter 6: The future of design systems

**P-DSH-32 Design states and data, not pictures.** Design at product fidelity, with real states, interactions and data, instead of one static picture of the ideal screen. Test: Each key screen has rendered empty, error and longest-content states, not only the ideal one.

Sources: Design Systems Handbook (InVision DesignBetter); Chapter 1: Introducing design systems, Chapter 2: Designing your design system, Chapter 3: Building your design system, Chapter 4: Putting your design system into practice, Chapter 5: Expanding your design system, Chapter 6: The future of design systems. Paraphrased in the kit's own words; no sentence is quoted.

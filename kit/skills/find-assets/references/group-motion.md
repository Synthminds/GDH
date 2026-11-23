# Group: motion

Catalog group `motion`: animation libraries, animation file players and programmatic video tools. Read this file at step 6 of `find-assets` when the need is a motion library, a player or an animation file.

How to read this file. An id is a catalog id. An id marked `*` has `verifiedOn` null: read its license before use. Every pick is a default from desk research. Evidence: UNTESTED in a build. License notes are DOCUMENTED on the catalog date, except where marked `*`.

What moves, how long and with which easing belong to `ui-motion`. Video scripts, storyboards and exports belong to `motion-video`. This file covers sourcing and license.

## First picks by need

| Need | Catalog ids | Why | Known limit |
| --- | --- | --- | --- |
| Page and state transitions with no dependency | `view-transitions`, `scroll-driven-animations` | Platform features: nothing to license, nothing to ship | Check browser support. Provide a fallback. |
| Component motion in React | `motion` | The usual choice for React, permissive license | Paid extras exist. Do not copy from them. |
| Timelines and scroll choreography | `gsap`, `animejs` | `gsap` is the most capable. `animejs` is small and permissive. | `gsap` is free and not open source, with a tool-type limit. Its full license text was not read. |
| Automatic list and layout transitions | `auto-animate` | One line for a common need | Little control |
| Smooth scrolling | `lenis` | The usual library | It can harm accessibility. Honor reduced motion. |
| Vector animation files with a small player | `dotlottie-web`, `lottie-web` | Players under a permissive license | `lottie-web` is a large bundle. Prefer the newer player. |
| Interactive, state-driven vector animation | `rive-runtime` | A state machine in the file | The editor is a hosted product with plan limits |
| Ready-made animation files | `lottiefiles-free*`, `rive-community*` | Large community catalogs | Uploads can infringe. Paid items use another license. `rive-community*`: credit required. Unread. |
| Hand-tuned sequences, often for 3D cameras | `theatre` | Keyframe sequencing with a visual editor | The editor package is AGPL. Keep it out of the production bundle. |
| Video written as code | `hyperframes`, `remotion` | `hyperframes` is permissive. `remotion` is the most complete. | `remotion` is free only up to an entity size. Larger entities need a paid license. |

## Decision rules

1. Platform first. Use a platform feature when it does the job on the browsers in the brief.
2. Then the smallest library that does the job. Default: one animation library for each project.
3. A second animation library needs a reason in `design/decisions.md`.
4. Reduced motion is a gate. A library or a file that cannot honor it does not ship.
5. Default: add smooth scrolling only when the brief asks for it.
6. Record each library as a package at one exact version.
7. For `gsap`: ask whether the product is a visual animation builder. When it is, read the full license. Verdict `needs a human`.
8. For `remotion`: ASK for the headcount of the entity that will use it. Record the answer in the manifest `note`.
9. For `theatre`: install the editor as a development dependency only. Confirm that the production bundle excludes it.
10. Prefer an animation file made for the product over a community file. A community file is someone's style.
11. For a community file, answer question 9 of the license decision: is the uploader the maker?
12. Timing and easing come from motion tokens, not from a library's defaults.

## License traps

- "Free" and "open source" differ. `gsap` is free of charge under its own license.
- An entity-size limit (`remotion`) depends on the client, not on the agency or the agent.
- A split license inside one project (`theatre`): the runtime is permissive, the editor is copyleft.
- Community animation catalogs mix free and paid items on similar pages.
- Platform features have no license. Documentation examples do: write your own code.
- A player's license says nothing about the animation file it plays.

## Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Library defaults | Every motion uses the library's default duration and easing | Set both from motion tokens |
| Three engines | Two animation libraries plus a scroll library for one page | Reduce to one, or to platform features |
| Editor in production | A development editor in the shipped bundle | Move it to development dependencies. Check the bundle. |
| Stock animation | A well-known community animation as a brand moment | Make the moment for the product |
| Scroll hijack | Scrolling that no longer follows the input | Remove it, or limit it to one section with a way out |
| No reduced-motion path | Motion that ignores the user setting | Add the path. `accessibility-gate` checks it. |

## Worked choice

The outcomes below are illustrative. They show the reasoning, not verified facts about a source.

Need: section reveals on scroll and a number that counts up, for a marketing page. Brand words: calm, exact. Ships in a client product. Browsers: current evergreen.

- Platform first: scroll-driven animation covers the reveals on the browsers in the brief, with a static fallback.
- The counting number needs a few lines of script. No library is needed for it.
- Rejected: a timeline library. It can do both, but nothing here needs a timeline, and it adds a license to track.
- Rejected: smooth scrolling. The brief does not ask for it.
- Result: no outside asset. Durations and easing come from the motion tokens. The reduced-motion path shows the final state at once.

# Platform conventions and navigation models

Read this file at steps 8 and 11 of `app-design`. It lists the conventions of iOS, Android, desktop and web apps, and it gives the rules for choosing a navigation model.

## 1. How to use this file

Every platform value here is a default. None is a gate.

Evidence classes:

| Class | Meaning | How to treat it |
| --- | --- | --- |
| Read | A primary source was read during the research | A sound default |
| Search | A search result confirmed it; the page was not opened | A default. Confirm before you depend on it |
| Memory | Stated from memory of the platform guide | A default. Read the current guide before release |
| Rule of thumb | Practitioners repeat it; no primary source sets it | A starting value only |

Precedence: the user, then the project design system, then the brief, then these defaults. The gates in `SKILL.md` hold on every platform.

Platform looks change every year. Before release, read the current Apple Human Interface Guidelines or Material Design guide for the release you target. Label the result DOCUMENTED with the date.

The principle: same job, native control. The brand lives in tokens: color, type, shape, voice, imagery. Navigation, controls, gestures and base type sizes follow the platform. A person who knows the platform already knows half of your app.

## 2. iOS and iPadOS

| Topic | Default | Class |
| --- | --- | --- |
| Top-level navigation | A tab bar for three to five peer places | Memory |
| Drill-down | A navigation stack. Back sits at the top leading edge. A swipe from the leading edge also goes back | Memory |
| Contained tasks | A sheet for a task that starts and ends in one place | Memory |
| Targets | 44 by 44 pt or more. A small icon may sit in a larger tappable area | Search |
| Body text | 17 pt. Nothing below 11 pt | Memory |
| Text scaling | Text follows the system text size setting. Layouts reflow at large sizes | Memory |
| Safe areas | Content clears the notch, the home indicator and rounded corners | Read: Vercel, for the web form of this rule |
| Gestures | Pull to refresh, swipe actions on rows, edge swipe to go back. Each has a visible control too | Memory, plus the gate in `SKILL.md` |
| Destructive actions | Marked as destructive and confirmed, or reversible | Memory |
| System materials | A translucent material separates a layer from content that moves under it. It is not decoration | Read: Impeccable craft floor, for the decoration rule |
| Icons | The system symbol set has its own license terms. Read them before use outside the platform | Memory |

Notes for 2026. A new system material arrived with the 2025 releases of iOS and macOS, and the guide was updated for it (search). One search result reports a further revision in 2026. That report is unverified. Treat any stored knowledge of the current look as possibly dated.

## 3. Android

| Topic | Default | Class |
| --- | --- | --- |
| Top-level navigation | A bottom navigation bar for three to five places on a compact width | Memory |
| Wider windows | A navigation rail at medium widths. A drawer or a permanent side list at expanded widths | Memory |
| Back | The system back gesture or button always works and goes where the person expects | Memory |
| Primary action | One prominent action for a screen, placed for the thumb | Memory |
| Targets | 48 by 48 dp or more | Search |
| Spacing between targets | 8 dp | Rule of thumb |
| Body text | 16 sp. Sizes in sp, so text follows the system setting | Memory |
| Layout units | dp for layout. Window size classes decide the layout, not device names | Memory |
| Color | The platform can derive colors from the user's wallpaper. Decide whether the brand palette or the user's palette leads | Memory |
| Edge to edge | Content draws behind system bars, with insets respected | Memory |
| Motion | The 2025 revision of the platform's design language moved motion toward spring physics | Memory |

ASK when the brief is silent on dynamic color: "Does the app keep the brand colors, or follow the user's system colors?" The answer changes the token set. Check contrast for both when both are possible.

## 4. Desktop: macOS and Windows

A desktop app is used with a pointer and a keyboard, for long sessions, in a window that the person resizes.

| Topic | Default | Class |
| --- | --- | --- |
| Targets | 24 px or more for a pointer | Read: Vercel. See the target table in the forms reference |
| Keyboard | Every action is reachable by keyboard. Focus is always visible | Gate in `SKILL.md` |
| Shortcuts | Follow the platform: the Command key on macOS, the Control key on Windows. Never take over a system shortcut | Memory |
| Menus | macOS: commands also live in the menu bar. Windows: commands live in the window | Memory |
| Context menus | A secondary click offers the actions for the thing under the pointer. Each action also exists elsewhere | Memory |
| Hover | Hover states and tooltips exist. Nothing essential is hover-only | Read: Rauno Freiberg, Web Interface Guidelines |
| Windows | Resizable, with a stated minimum size. The layout adapts as the window narrows | Memory |
| Selection | Click selects one. A modifier click adds. A shift click selects a range | Memory |
| Undo | Undo and redo work for edits | Memory |
| Density | Denser than touch. See the density levels in the forms reference | Read: Emil Kowalski standards, on cohesion for professional tools |
| Drag and drop | Supported where natural, always with a non-drag way to do the same thing | Gate in `SKILL.md` |
| Motion | Little. Frequent, keyboard-driven actions do not animate | Read: Emil Kowalski standards |

## 5. Web apps

A web app runs in a browser. The browser's own behavior is the convention.

| Topic | Default | Class |
| --- | --- | --- |
| Addresses | Each view and state has an address: the open item, the tab, the filters, the page of a list | Read: Vercel |
| Links | Navigation uses real links. Open in a new tab works | Read: Vercel |
| Back | Back returns to the earlier state and restores the scroll position | Read: Vercel |
| Focus on route change | Focus moves to the new view's heading or main region | Memory: accessible routing practice |
| Browser features | Find in page, text selection, zoom and autofill keep working | Read: Vercel |
| Targets | 24 px for a pointer and 44 px for touch | Read: Vercel |
| Inputs | 16 px or more on mobile web. Autofocus is rare on mobile | Read: Vercel |
| Hover | Styles sit behind `@media (hover: hover)` | Read: Rauno Freiberg |
| Overlays | A modal or drawer contains its own scroll | Read: Vercel |
| Long lists | Virtualize or paginate past 50 items | Read: Vercel |
| Mutations | Respond in under 500 ms, or update optimistically with a way back | Read: Vercel |

## 6. One app on several platforms

1. Share the brand layer: tokens, voice, imagery, the names of things.
2. Share the flows and the screen jobs.
3. Split the control layer: navigation, back, sheets, menus, pickers, gestures, base type size.
4. Do not ship iOS patterns on Android, or the reverse.
5. Do not shrink a web layout onto a phone. Rebuild it from the narrow layout up.
6. Default for a single cross-platform target size: 48 by 48 with 8 between targets. It is the stricter of the two platform values (rule of thumb).
7. Write a platform column in the screen inventory. Note only what differs.

## 7. Choose the navigation model

Count the top-level places first. A place is somewhere a person returns to, not a task they finish.

| Model | Fits | Typical form | Avoid when |
| --- | --- | --- | --- |
| Tabs, flat | Three to five peer places that people switch between | A tab bar or a bottom bar on a phone | There are more than five places, or the places are steps of one task |
| Stack, hierarchical | Lists that drill down to detail | Push and back | The depth passes three levels. Flatten it, or add search |
| Sidebar | Many sections, a wide window, long sessions | A side list, collapsible | A phone. Use the adaptive pair below |
| Rail | Three to seven places at medium width | A narrow column of icons with labels | Labels would be cut |
| Drawer | Many places that are rarely visited | A panel behind a labelled button | The places are used daily. Hidden places are forgotten |
| Hub and spoke | Separate tools reached from one home | A home screen with entries | People move between tools often |
| Linear task | One job with ordered steps | A stepper, with progress and a way back | The steps are not really ordered |
| Command palette | Expert users on desktop and web | A search of actions, opened by a shortcut | It is the only way to reach an action |

Decision rules:

1. One or two places: no navigation bar. Put the second place in the top bar.
2. Three to five places on a phone: a tab bar or a bottom bar. Default, from memory of both platform guides.
3. More than five: rank them with the task ranking. Keep four, and group the rest under one labelled place.
4. One codebase across widths: a bottom bar at compact width, a rail at medium, a sidebar at expanded.
5. Labels come from the job stories. Every icon in the navigation has a text label.
6. The current place is marked by more than color.
7. A linear task hides the main navigation only when leaving would lose work. Then it shows how to exit safely.
8. Default: four choices at one decision point. A dashboard may show more metrics; that ceiling is in `dashboard-design`.

### Reach on a phone

- Place the primary action in the lower half of the screen.
- Keep a destructive action away from the primary action.
- A control at the top of a tall phone needs a second route for one-handed use. These three are rules of thumb.

## 8. System settings to support

| Setting | What the design must do | Class |
| --- | --- | --- |
| Text size | Text scales with the system setting. Default: up to 200 percent with no clipping or overlap | Memory: WCAG 2.2 |
| Dark mode | Its own token mapping, not an inversion. Check every pair again | Read: Vercel |
| Reduced motion | Movement is removed. Opacity and color may stay | Gate in `SKILL.md` |
| Higher contrast | Borders and text strengthen. Nothing relies on a subtle tint | Memory |
| Right to left | Layout mirrors. Icons that show direction flip | Memory |
| Screen reader | Every control has a name, a role and a state | See `accessibility-gate` |

## 9. Worked choice

The invented inspection app. Platforms: Android phones for technicians, a web app for the office.

- Top-level places for the technician: Today, Lifts, History, Profile. Four peers that people switch between. Model: a bottom navigation bar.
- "Start inspection" is not a place. It is the primary action on Lift detail, in thumb reach.
- The office web app has seven sections and long sessions. Model: a sidebar. Each view has an address, so a manager can send a link to one lift.
- Shared: tokens, the names "lift", "inspection" and "due", the status colors with their icons.
- Split: the phone uses the system back gesture and bottom sheets. The web app uses links, Back and a table with keyboard selection.
- Dynamic color: asked. The answer was "keep the brand colors". Status colors must stay stable for safety.
- Rejected: a drawer on the phone. All four places are used daily, and a drawer hides them.

## 10. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Shrunk web | Small targets, hover-only controls and top-heavy actions on a phone | Rebuild from the narrow layout |
| Wrong platform | An iOS tab style on Android, or the reverse | Split the control layer |
| Custom control | A hand-built picker that ignores back, selection or text scaling | Use the platform control. Theme it with tokens |
| Glass for fashion | Blur and translucency with no moving content beneath | A solid token surface |
| Hidden daily place | A daily destination inside a drawer or a "More" list | Promote it |
| Fixed type | Text sizes that ignore the system setting | Platform units that scale |
| Animated everything | A transition on every tap | Remove motion from frequent actions. See `ui-motion` |
| Stale guide | A platform look taken from memory | Read the current guide. Date the note |

## 11. Checks

Gates: see `SKILL.md`. This file adds none.

Defaults:

- Default: 44 pt targets on iOS, 48 dp on Android, 24 px for a pointer.
- Default: three to five top-level places on a phone.
- Default: body text at the platform size, scaling with the system setting.
- Default: every platform value is confirmed against the current guide before release.

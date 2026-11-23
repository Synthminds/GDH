---
status: template
updated: YYYY-MM-DD
---

# Design handoff

The `handoff-to-code` skill fills this file. It is the package for the coding harness or any coding agent.
Give reasons, not only values: each section says why, so the builder can solve what this file did not foresee.

## 1. What to build

Scope in one paragraph. Screens or assets in scope, ranked. What is out of scope.

## 2. Source files

| File | Holds | Status |
| --- | --- | --- |
| `DESIGN.md` | The design system in prose | |
| `design/tokens.json` | Token values | |
| `design/tokens.css` | Generated custom properties | |
| `design/brief.md` | Audience, job, brand words, constraints | |
| `design/decisions.md` | Chosen direction and rejected options | |
| `design/assets/manifest.json` | Asset provenance and licenses | |

## 3. Decisions the build must keep

List each decision with its reason and its decision record entry. Mark each brand-required choice.

## 4. Screens, states and breakpoints

### 4.1 Components

One row per component. Give each prop a type, whether it is required, and its default.

| Component | Status | Props | Variants | States | Tokens | Reference file | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

### 4.2 Screen state matrix

One row per screen. Mark each cell `designed`, `n/a` or `not designed`.

| Screen | Loading | Empty | Partial | Error | Success | Offline | Permission denied | Not found | Session expired |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

### 4.3 Layout and breakpoints

One row per breakpoint. Use the design system's breakpoints when it has them.

| Name | Min width | Columns | Gutter | Container | Changes |
| --- | --- | --- | --- | --- | --- |

### 4.4 Content and the copy deck

One row per string, grouped by screen. Link a separate deck file here when the copy is long.

| Key | Screen | Text | Notes |
| --- | --- | --- | --- |

### 4.5 AI runtime sheet

Fill this only when the design includes a model-driven feature. Otherwise write "Not in scope."

| Area | In scope | Design decision | Code decision | Stage |
| --- | --- | --- | --- | --- |

## 5. Motion

| Element | Trigger | Duration token | Easing token | Reduced-motion behavior |
| --- | --- | --- | --- | --- |

## 6. Assets

List each asset by manifest id, with format, size and where it is used.

## 7. Acceptance checks

List the gates the build must pass. Name the check and how to run it.

## 8. Simplifications

List each simplification made for build reasons, what the user loses, and who accepted it.

## 9. Open questions

List each open question with who can answer it.

## 10. Evidence

State what was VERIFIED, what is DOCUMENTED and what is UNTESTED in this package.

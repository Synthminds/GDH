# 0001: GDH is a sibling kit, not a part of GCH

Date: 2026-11-23. Status: accepted.

## Context

The coding harness GCH carried a small design surface and wired third-party design skills. The owner wants deep design work: brand, mood boards, design systems, charts, 3D, motion, and many design tools that spend credits. Three facts decide where that work lives.

1. The GCH check, build and export engine reads only its own package kit.
2. The GCH tool catalog accepts pinned local servers only. Design tools are mostly hosted connectors with a sign-in and paid credits.
3. The GCH always-on text budget is nearly used. Design skills inside GCH would crowd out coding skills.

## Decision

GDH is its own repository and its own plugin, with its own registry, kernel, catalogs, check engine and export. It has no hard dependency on GCH.

- GDH reimplements the kit rules it needs in one Python file with no dependency.
- GDH copies no GCH code and no GCH prose. It follows the same shape: registry, kernel, moments, one code for each rule, an export with a managed block.
- GCH keeps its screen rules and its evidence captures. It gains one wired entry and one moment that offers GDH.
- When both kernels are loaded, GCH governs code work and its screen numbers hold. The GDH kernel says so in one line.
- GDH keeps its own budgets small: five model-invoked skills, a kernel of 60 lines, a moments text of 3,500 characters. Amended 2026-11-23 by [0005](0005-align-opens-every-session.md): six model-invoked skills, with `align` added.

## Consequences

- Each harness can be installed, versioned and checked alone.
- Two SessionStart texts load when both are installed. The budgets must stay small on both sides.
- The boundary needs a written contract. It is in `docs/HANDOFF-GCH.md`.
- Some rules exist twice in spirit: the accessibility floor and "find the design system first". The two texts must not contradict each other.
- The GCH-side change is a proposal until it is applied and checked in that repository.

## Alternatives considered

- Design skills inside the GCH kit: rejected for the budget and the catalog reasons above.
- A GCH extension: rejected, because the extension mechanism installs commands and rules for one host and carries no skills.

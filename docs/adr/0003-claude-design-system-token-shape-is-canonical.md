# 0003: The Claude Design System token shape is the canonical token file

Date: 2026-11-23. Status: accepted.

## Context

The owner asked for design systems "just like the Claude Design tool". A project also needs tokens that any agent on any host can read from disk, and that a build can consume. Several token formats exist: the hosted Design System shape, the community design-tokens format, CSS custom properties and framework theme files.

## Decision

`design/tokens.json` in a project, and `tokens.json` in a brand pack, use the Claude Design System shape:

- each family is a list of `{name, value, usage}`;
- `color` holds `themes` and tokens whose value can differ for each theme;
- `type` holds `fonts`, `families` and `groups` of styles.

One script, `ds.py`, owns the shape. It validates a file, measures contrast for the text and ground pairs named in usage notes, converts from CSS custom properties and from the community token format, converts to that format, exports CSS and a framework theme file, writes `DESIGN.md` with YAML front matter, writes a specimen page and audits source files for raw values.

Everything else is generated from the token file: `tokens.css`, `DESIGN.md`, the specimen. Nobody edits a generated file.

## Consequences

- A brand pack can be published as a hosted Design System without a conversion step, and a hosted system can be brought to disk in the same shape.
- The usage note on every token is required. It tells an agent when to use the token, and it feeds the contrast check.
- Agents outside Claude read the same file. A local pack is always kept beside a hosted system.
- Conversion loses some things. The script reports each value it could not convert and does not guess.
- The shape is owned by a product that can change it. The publish and sync protocols are DOCUMENTED and were never run against a live account. A change on the product side means a change in `ds.py` and its tests.
- A design system that was moved from the old standalone site can lack a token file. It must be converted before other artifact types can install it.

## Alternatives considered

- The community token format as the canonical file: rejected. It has no usage note for each token and no theme list in the form the hosted types read. `ds.py` converts both ways instead.
- CSS custom properties as the source: rejected. They carry no usage notes and no type styles.

# Extract a system from an existing product

Use this when a product exists and its styles hold raw values. Measure first, then extract. Skip the audit only when no product exists yet.

`DS` means `python3 <skill folder>/scripts/ds.py`.

## Step 1: the visual inventory

1. Run `DS audit <source folders> --inventory --json`. It reads CSS, HTML, JSX and TSX.
2. Report the counts to the owner in plain numbers: unique colors, font sizes, font families, spacing values, radii, durations.
3. Report token definitions and token references. They show how far the product already uses variables.
4. Show the near-duplicate color groups. Each group is a merge candidate.
5. Save the JSON as the baseline. You will run the same command at the end.

Limits of the audit. Say them in the report:

- It counts literals in source text. It does not see values computed at run time.
- It does not count named colors such as `red`.
- It does not read Sass variables, CSS-in-JS helpers or a Tailwind config file. Read those by hand.

## Step 2: the UI inventory

1. List every element kind in the product: buttons, inputs, cards, tables, navigation, dialogs.
2. Capture each variant. Use a tool with the `capture` capability, or ask the owner for screenshots.
3. ASK: mark each variant keep, merge or remove.
4. The kept list is the component inventory. Build nothing that is not on it.

## Step 3: extract tokens

1. Product already has custom properties: run `DS from-css <files> --name "<Name>" -o design/tokens.json`. Read the full report.
2. Product has a token file: run `DS from-dtcg`.
3. Product has only raw values: group the audit values by role with the owner.
   - ASK for each near-duplicate group: "Which value is intended?"
   - Keep the product's real values. Do not snap them to a new scale without a yes.
   - Name each token by role.
4. Write a usage note on every token from how the code uses it.
5. Run `DS validate` and `DS contrast`. A failing pair is a finding about the product. Report it; fix it only with a yes.

## Step 4: the brand book and generated files

1. Write the README from what the code does, as usage rules.
2. Generate `tokens.css`, `DESIGN.md` and the specimen.
3. Record provenance in `SOURCE.md` and in `tokens.json` under `meta`: repository, commit or date, and files read.

## Step 5: hand the replacement to the coding harness

This skill does not edit product code. Write the plan into `design/handoff.md`:

1. The token file and `tokens.css`.
2. A map from each raw literal to its token, from `DS audit <folders> --tokens design/tokens.json --json`.
3. The literals with no token, and the decision for each.
4. Default: replace by family, colors first, and compare screenshots before and after each family.

When GCH is loaded, GCH governs the code change. Call its skills for the edit and the review.

## Step 6: measure again

1. After the code change, run `DS audit <folders> --tokens design/tokens.json`.
2. Report raw literals before and after. The target is zero. Each remaining literal needs a reason.

## A re-sync later

- Run `from-css` again into a scratch file. Compare it with the pack.
- Keep usage notes and README prose. Update changed values.
- List tokens the code dropped. ASK before you remove one.

## Sources

- Design Systems Handbook (InVision DesignBetter), chapter 2 "Conducting a Visual Audit" and "Creating a user interface library"; chapter 3 "Automating code style".
- Claude Design System artifact type, from-code reference, read 2026-11-23.

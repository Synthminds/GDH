# GDH eval cases

`gdh.py check` proves the form of the kit. A triggering case measures behaviour: does a model-invoked skill start on a plain user prompt? The quality corpus measures the tell scan and the mood-board diff.

This folder holds the cases only. GDH ships a static validator and no runner. The case format follows the GCH triggering suite, so a GCH eval runner can read the cases when it gains a kit-root option. Evidence: UNTESTED. No runner has read these files.

## Layout

```
evals/cases/triggering/<id>.json    one case in each file
```

## Case format

```json
{
  "id": "trigger-mood-board",
  "kind": "triggering",
  "skill": "mood-board",
  "prompt": "We open a bakery next month. Show me what the shop site could look like.",
  "expect": {"skills_fired": ["mood-board"]}
}
```

| Field | Rule |
| --- | --- |
| `id` | Equals the file name without `.json`. |
| `kind` | Always `triggering`. |
| `skill` | The model-invoked skill that the prompt must start. Write `none` for a negative case. |
| `prompt` | The words of a user. |
| `expect` | What a grader reads. `skills_fired` is a list that holds the case skill. |

`gdh.py check` reports a case that breaks one of these rules as `GDH_EVAL_CASE`.

## Negative cases

A negative case holds a prompt that must start no GDH skill. Example: a backend bug fix.

```json
{
  "id": "negative-backend-bug-fix",
  "kind": "triggering",
  "skill": "none",
  "prompt": "Find the bug in the date parser, fix it and add a regression test.",
  "expect": {"skills_fired": [], "skills_not_fired": ["ask-gdh", "design-brief"]}
}
```

- `skill` is `none` and `skills_fired` is empty. `check` enforces both.
- `skills_not_fired` is optional. It names the skills a grader watches for.
- The second negative case in this folder is the small-change exit: a contained change inside an existing design system is code work and must start no GDH skill.

## Rules for a case

1. Write the prompt as a user writes. Do not reuse the words of the skill description.
2. Give the prompt something to act on: a product, an audience or a file.
3. Do not name the skill in the prompt.
4. Write two cases or more for each model-invoked skill. `gdh.py doctor` reports a skill without a case as `GDH_DOCTOR_NO_EVAL`.
5. Keep private data out of a prompt. The repository is public.

## Commands

```
python3 scripts/gdh.py check      validate every case
python3 scripts/gdh.py doctor     list model-invoked skills without a case
python3 scripts/gdh.py new-skill <name> --invocation model --discipline <d> --description "<text>"
```

`new-skill` writes a case stub for a model-invoked skill. Replace the stub prompt before you rely on the case.

## Quality corpus

`gdh.py check` and the triggering cases do not measure the owner's first requirement: output that is not the default look. The quality corpus measures the two scripts that guard it.

```
evals/cases/quality/labels.json           the labels and the recorded baseline
evals/cases/quality/fixtures/*.html       labelled pages
evals/cases/quality/boards/*.json         labelled mood boards
python3 evals/quality.py [--json]         score; exit 1 when a measure falls below the baseline
```

- Page classes: `generic-first-wave`, `generic-second-wave`, `brand-required` (with the brand tokens beside the page) and `distinctive` (hand-made pages).
- Each page lists the `tells.py` codes a careful critic would flag. The scorer reports precision and recall for each rule and for whole pages.
- Each board lists the pair verdicts and the error codes of `moodboard.py diff`: the passing ferry board, three skins of one idea, and three default looks.
- `tests/test_quality.py` runs the scorer in the unit suite. A change that lowers a score fails the suite. When a rule improves, raise its value in `baseline`.
- Record the scores in `kit/skills/design-critique/refinement-log.md` whenever the tell list changes.
- Evidence: the labels are one reviewer's judgment on 10 pages. Treat the numbers as a regression guard, not as a measure of taste.

## Reading a result

A triggering result needs about 10 runs for each case before a difference means much. Under 3 runs, treat the result as a check of the harness, not of the skill. Default: both numbers come from the GCH eval notes and are not measured here.

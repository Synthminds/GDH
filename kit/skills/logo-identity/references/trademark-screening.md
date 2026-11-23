# Trademark screening: the knockout search and its limits

Read this file at step 12 of `logo-identity`. It covers what a knockout search is, what it cannot do, when to run it, the procedure, the record file, the report wording and the failure patterns.

This file is not legal advice. The agent is not a lawyer. A knockout search finds obvious conflicts. It clears nothing. The user confirms with a trademark attorney before a name or a mark is adopted, registered or launched.

Evidence. The procedure follows step 7 of the license rules in the GDH asset research. The search services are entries of the asset catalog, group `logo-aids`. Their terms and their current features were not read: each has `verifiedOn` null. Read the service's own page through `find-assets` before first use. General statements about trademark practice in this file are common knowledge written from memory. They are defaults, and a lawyer's word replaces them.

Terms. A knockout search is a first search for identical or near-identical marks. A register is the database of one trademark office. A class is a category of goods or services in a register. Clearance is a lawyer's opinion that a mark may be used.

## 1. What the search can and cannot do

| It can | It cannot |
| --- | --- |
| Find identical names in the registers searched | Find marks used without registration |
| Find close spellings and sound-alikes you thought to try | Find every variant a court would call similar |
| Find the same name in the same field on the web and in app stores | Cover a country whose register was not searched |
| Give the user and counsel a starting list | Judge the likelihood of confusion; that is a legal judgment |
| Show that a mark is crowded or common in a field | Say that a mark is free, safe or available |

State these limits with every result. Never write "the name is free", "cleared" or "available".

## 2. When to run it

| Moment | Search | Why |
| --- | --- | --- |
| Before any drawing, when the name is new | The name | A name conflict discards every wordmark |
| After the direction is chosen, before the system is built | The name again, and the look of the mark | The cheapest moment to change |
| Before delivery | Confirm that the record exists and counsel is named or pending | The gate |

A user can decline the search. Then write that in the decision record and in the report. Do not present the mark as screened.

## 3. Before you search

1. ASK for the countries that matter and the goods or services the mark will cover.
2. ASK whether a lawyer already works on the mark. If so, give the lawyer the list. Do not duplicate paid work.
3. GATE: an image search uploads the unreleased mark to a third party. Ask before any upload. A text search of a name also reveals the name to the service. Say so when the name is secret.
4. Read the terms of each search service through `find-assets`. A service with unread terms is a lead, not a tool.
5. A service may be a public register, a network of registers or an international database. Record which one you used.

## 4. The procedure

1. Write the search list for the name:
   - the exact name
   - the name with and without spaces or hyphens
   - sound-alikes: other spellings that are said the same way
   - common misspellings and plurals
   - the distinctive part alone, without descriptive words
   - a translation, when the name is a word in a market's language
2. Find the classes for the goods and services. Use the register's own class finder. ASK the user to confirm them.
3. Search each term in each register, first in the chosen classes, then in all classes.
4. Note each hit: the mark, the owner, the register, the class, the status, the record number or link.
5. Sort the hits: identical in the same field; similar in the same field; identical in another field; the rest.
6. Search the web and the main app stores for the name with the field's key words.
7. Check the company name register of the home country, the domain and the main social handles. These are not trademark rights. They show crowding.
8. For the look of the mark, only after the user's yes: use a register's image search, when one exists. Describe what you compared.
9. Compare the mark with the competitor sheet again.
10. Do not judge similarity. Report what you saw, side by side.

## 5. The record file

Write `design/reviews/<date>-trademark-knockout.md`:

```
# Trademark knockout search: <name>, <date>

Not legal advice. This search finds obvious conflicts only. It is not clearance.
Counsel: <name of the firm or "not yet engaged">.

Scope
- Name searched: <exact form>
- Variants searched: <list>
- Goods and services: <description>; classes: <numbers, confirmed by the user on date>
- Registers searched: <service, country or region, date>
- Not searched: <countries, registers, unregistered use, image similarity unless stated>
- Image search: <not run | run on date with the user's yes, service>

Hits
| Mark | Owner | Register | Class | Status | Link or number | Group |

Other findings
- Web and app stores: <what was found>
- Company names, domains, handles: <what was found>

Result
<one of the two forms below>
```

Keep screenshots or exported result lists beside the file. A register changes daily. Date everything.

## 6. Report wording

Use one of two forms. Add nothing that sounds like clearance.

- "No obvious conflict found in <registers> for <name> and <n> variants in classes <numbers>, on <date>. This is not legal clearance. Unregistered marks, other countries and similarity judgments are not covered. A trademark attorney must clear the mark before launch."
- "Possible conflict: <mark>, owner <owner>, <register>, class <number>, status <status>. I do not judge whether it blocks the name. Show this to a trademark attorney before you go further."

Then ASK: "Do you want to continue with this name while counsel reviews it, pause, or look at other names?"

Record the answer in `design/decisions.md`. Work that continues before clearance is at the user's risk. Say so once, plainly.

## 7. Design choices that affect registrability

These are general points for the user's talk with counsel. They are not advice.

1. A name that only describes the product is weak as a mark. A coined or unexpected word is stronger.
2. A symbol built from a stock icon cannot be owned exclusively. Others hold the same file. Some icon licenses forbid logo use.
3. A mark that includes another organization's mark, a flag, an official seal or a protected emblem causes trouble. Leave them out.
4. A typeface license can limit logo and trademark use. The manifest record must show that it allows it.
5. A generated starting point can affect protection in some countries. Tell counsel when a candidate was generated.
6. Keep the dated concept sheets and the decision record. They show how the mark was made.
7. A registration covers the form filed. Ask counsel whether to file the wordmark, the symbol, or both, and in which colors.

## 8. Checks

1. The record file exists, is dated, and names the registers and the classes.
2. The limits are stated in the file and in the closing report.
3. The words "free", "cleared", "available" and "safe" do not describe the mark anywhere.
4. Every upload had a yes.
5. The user's decision after the result is in `design/decisions.md`.
6. The closing report says "Counsel: confirmed" or "Counsel: pending".

## 9. Failure patterns

| Name | Sign | Fix |
| --- | --- | --- |
| Clearance claim | "The name is free" after a register search | Use the report wording. State the limits. |
| Exact match only | Only the exact spelling was searched | Add sound-alikes, variants and the distinctive part |
| One register | A home-country search for a brand that sells abroad | Search each market's register, or list it under "Not searched" |
| Wrong classes | Classes guessed and never confirmed | Use the class finder. Ask the user. |
| Leaked mark | An unreleased logo uploaded with no question | Exposure gate, every time |
| Judging similarity | "This one is different enough" | Report both marks. Counsel judges. |
| Search at the end | The first search runs after the system is built | Search the name before drawing |
| Undated result | A hit list with no date | Date the file and each search |
| Silent skip | The search was declined and the report does not say so | Record the decline. Report "not screened". |

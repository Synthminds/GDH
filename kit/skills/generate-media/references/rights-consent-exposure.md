# Rights, consent and exposure

Read this file at steps 8 and 9 of `generate-media`. It covers what generation may not imitate, consent for likeness and voice, the tool's output terms, the exposure rules for uploads of client material, feedback tools, and AI-content disclosure.

Evidence. The exposure gate is kernel rule 6. The connector facts (chat attachments are not visible to a server, so the agent uploads bytes itself; some tools forbid pushing private or generated files to third-party hosting to make a URL; feedback tools send data to the vendor, sometimes with the user's name and workspace; jobs can end in a safety or IP-detected state) come from the connector cards, read 2026-11-23. No research source stated how long any connector keeps uploaded files; treat retention as unknown. The disclosure rules come from vendor blogs that disagree. Nothing here is legal advice.

## 1. What generation may not imitate

| Do not generate | Why | Instead |
| --- | --- | --- |
| A real, identifiable person without written consent | Likeness and publicity rights; deception | A consenting person's photos; or no person |
| A public figure, actor or celebrity | Rights and deception, with or without consent from others | No person, or a licensed photo used within its terms |
| A living artist's style by name | Imitation of a person's work; many tools forbid it | Describe the technique in words |
| Another brand's logo, character, product or packaging | Trademark and copyright | The client's own assets |
| A copyrighted character or scene | Copyright | Original work |
| A fake customer, testimonial, award or certificate | Kernel rule 11: invent nothing factual | A labelled placeholder until real proof arrives |
| A screenshot of a product interface | Invented facts about the product | A real capture |
| A real place presented as the client's | Misrepresentation | The client's photo |

When a tool ends a job in a safety or IP-detected state, do not rephrase to get around it. Tell the user and change the prompt sheet.

## 2. Consent for likeness and voice

GATE: no call that uses a real person's face, body or voice without that person's written consent on record.

A consent record is an ordinary entry in `design/decisions.md`, in the fixed entry format of the project template. Its scope starts with `consent,`. `round <n>` and `Stage:` are those of the current round, so a tool that reads the stage of the last entry still finds one. Scope, tool, terms and revocation go in `Keep / Change / Remove`. Where the signed document lives goes in `Open`.

```
## 2026-11-23 round 3: consent, voice clone for product videos
Stage: refine
Shown: consent terms for a voice clone
Feedback asked: Does the person give written consent for this scope?
Keep / Change / Remove: scope: keep (clone of voice from 3 supplied recordings, used in product videos for 12 months); tool: keep (<tool name>, its terms read 2026-11-23); revocation: keep (on request; delete the cloned voice in the tool and the generated files)
Decision: consent granted (by <person or role, as the user wants it recorded in this repository>)
Rejected: none
Open: the signed consent lives in <the user's own records; not in this repository>; review on 2027-11-23
Evidence: DOCUMENTED signed consent held by the user; UNTESTED clone output
```

A revocation is a new entry of the same shape with `Decision: consent revoked (by <who>)`. Never edit the old entry.

Rules:

1. Consent names the scope: what is made, where it is used, for how long.
2. Keep the signed document out of a public repository. Record only where it lives.
3. Consent from a company is not consent from the person.
4. A minor needs a guardian's consent, and a reason to appear at all.
5. When consent is revoked, delete the clone in the tool and the generated files, and record it.

## 3. The tool's output terms

1. Read the tool's terms for generated output before the first call of a project. Record the URL and the date.
2. Check: commercial use allowed; who owns the output; any attribution or label duty; restrictions on use in ads, logos or trademarks; whether inputs and outputs may be used to train the vendor's models.
3. Some places give weak or no legal protection to machine-made work. A generated asset may be hard to protect as the client's property. Tell the user when it matters (a mascot, a signature illustration).
4. A generated output can resemble existing work by chance. The tool does not clear it. For a central brand asset, run a reverse image search with the user's yes; that search uploads the image, so it is exposure too.

## 4. Exposure: uploads of client material

GATE: ask before any of the following leaves the project:

| Leaves the project | Examples |
| --- | --- |
| Client files | Product photos, CAD, unreleased designs, documents, recordings |
| Brand files | Logos, brand guides, unpublished campaigns |
| People's data | Photos of staff or customers, voice samples |
| Project content | Screens of an unreleased product, copy under embargo |
| Feedback to a vendor | A tool's feedback or rating call |

The ask names four things:

```
Upload check
What: 3 product photos of the unreleased planter (no people, no metadata)
To: <tool name>, as references for one generation job
Kept: the tool does not state how long it keeps uploads
Why: the generated scene must show the real product
Proceed? (yes / no / use fewer)
```

Rules:

1. Upload only what the job needs. Crop out unrelated content. Fewer files is better.
2. Strip metadata (location, camera serials, author names) before upload when the tool does not need it.
3. Never upload confidential documents, credentials, contracts or personal data as references.
4. A file in a chat attachment is not visible to a connector server. Upload the bytes through the tool's upload flow, or the tool's upload widget, as its card says.
5. Do not push a private or generated file to a third-party host only to create a URL for a tool. Use the tool's own upload.
6. Record each approved upload in `design/decisions.md`: what, to which tool, the date, the yes.
7. Feedback tools send data to the vendor. Call them only on the user's request, with no client content, code, paths or prompts.

## 5. AI-content disclosure

1. Platforms ask creators to label realistic generated people, voices and scenes. The rules differ and change; the sources found disagree.
2. Default: plan a label whenever a delivered asset shows a realistic generated person, uses a cloned or designed voice, or shows a realistic generated scene that a viewer could take as real.
3. Check the platform's own help page before publishing. `motion-video` handles video uploads.
4. Some clients require an internal disclosure of generated assets in deliverables. The manifest origin `generated` supports that.
5. Alt text describes what the image shows. It need not say "AI-generated", unless the client or platform asks.

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Lookalike person | A generated face that resembles a real person | No identifiable people without consent; regenerate |
| Style theft | "In the style of" a living illustrator | Technique in words |
| Silent upload | Client photos sent with no ask | The upload check, logged |
| Upload everything | A whole brand folder sent as references | Only what the job needs |
| Metadata leak | GPS and author data in uploaded photos | Strip metadata |
| Consent in the repo | A signed release committed to a public repository | Record where it lives, not the document |
| Terms unread | A generated mascot whose terms forbid trademark use | Read and record the terms first |
| Feedback leak | Project details sent in a vendor feedback call | Only on request; no client content |

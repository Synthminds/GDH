# When generation beats a licensed asset

Read this file at step 2 of `generate-media`. It covers the three routes (license, code, generate), the decision table by asset kind, the costs each route carries, and worked decisions.

Evidence. The license facts (CC0 sources are the lowest risk; stock sites forbid AI training and bulk collection; people, logos and property in free photos are not cleared) come from the GDH asset research, checked per source on 2026-11-23. The generation risks (catalog churn, uncertain result lifetimes, jobs that end in a safety or IP state, invented backs on single-photo 3D) come from the connector cards. The judgment that a brand-specific asset is where generation pays is this kit's own rule, built on the tell lists of the frontend-design skill and the Impeccable craft floor.

## 1. Three routes

| Route | What it is | Strength | Weakness |
| --- | --- | --- | --- |
| License | A photo, icon set, model, font or track with a license read and recorded | Known rights; real people and places; often free | Others use the same asset; may not fit the direction |
| Code | Made from tokens: SVG shapes, CSS gradients and grain, procedural 3D, charts, diagrams | Exact brand fit; tiny; editable; no rights question | Cannot make photographs or realistic scenes |
| Generate | A new image, clip, sound or model from a model | Unique; made to the brief; fills gaps that do not exist | Spends credits; rights and consent questions; inconsistent sets; artifacts |

Try them in this order: license, then code, then generate. Generate only when the first two cannot serve, or when uniqueness is the point and the user agrees to the cost.

## 2. Decision by asset kind

| Asset | First route | Generate when |
| --- | --- | --- |
| Icons | License one set, or draw in code | Never for a system icon set; a custom illustrative icon set may start from generated concepts, then redrawn |
| Logo | `logo-identity` draws it | Concepts only, inside that skill |
| Patterns, textures, grain, gradients | Code | A material texture that code cannot make (paper, stone, fabric), tileable |
| Abstract hero art | Code (shapes, shaders, gradients from tokens) | The direction calls for a painted or photographic abstract look |
| Photo of a real place, person or product | License, or the client's own photo | Never as a stand-in for the real thing. A generated "customer" or "office" misleads. |
| Conceptual or editorial photo (a mood, a metaphor) | License | No licensed image fits the direction, and the user agrees |
| Product shot of the client's product | The client's photos | Staged scenes around the real product, from the client's product photos as references |
| Illustration set | A licensed set when one fits; else commission or generate | A unique set in the brand's style; plan for consistency |
| Data chart or diagram | Code, through `data-viz` | Never |
| UI screenshot | Real capture | Never; a generated interface is invented |
| B-roll footage | License | Specific scenes no library has; abstract motion backgrounds |
| Voice-over | A human voice actor, or a library voice | A library or designed voice; a clone only with consent |
| Music bed | License | A custom bed of exact length and mood |
| Sound effects | License a free set | A specific effect no set has |
| 3D model | License | The client's real product from photos; a stylized object no library has |

## 3. Questions that decide

Ask in order. The first clear answer decides.

1. Does the asset depict a real person, place, product or event? Use the real thing: the client's photo, a licensed photo, a real capture. Generation would invent a fact.
2. Can it be made from tokens in code? Make it. It will match the brand exactly and cost nothing.
3. Does a licensed asset fit the direction after cropping, color treatment and composition? License it.
4. Is uniqueness part of the brief, or is the needed asset missing from every library? Generate, with the user's yes on the spend.

## 4. Costs to state before choosing generation

| Cost | Say to the user |
| --- | --- |
| Credits | The quoted cost per output and for the likely number of rounds |
| Time | Rounds of test, review, selection and finishing |
| Consistency | Extra work to keep a set matching |
| Rights | The tool's output terms; weaker legal protection for machine-made work in some places; no clearance of resemblance |
| Disclosure | Platforms may require an AI-content label for realistic people, voices or scenes |
| Maintenance | A later change needs the same tool and model, which may have changed |

## 5. Worked decisions

| Request | Decision | Reason |
| --- | --- | --- |
| "A hero image of happy customers using the app" | License a real photo, or use real customers with consent; or design a hero without people | Generated customers are invented people presented as users |
| "Grainy gradient background in brand colors" | Code | Tokens plus CSS or SVG noise; exact and free |
| "An illustration set of 12 spot illustrations in our style" | Generate after a one-image test, with a strict style kit; or commission | No licensed set has the brand style; consistency is planned |
| "A photo of our product on a marble counter" | Generate a staged scene from the client's product photos | The product is real; the setting is staging. Check the product is faithful. |
| "Our office building for the about page" | The client's own photo | A generated building misrepresents a real place |
| "A 20-second calm music bed" | License from a library, or generate if no track fits the length and mood | Both are fine; license is cheaper when a track fits |
| "A voice-over in our founder's voice" | Record the founder, or clone with the founder's written consent | No consent, no clone |
| "A bar chart of revenue growth" | Code with real data through `data-viz` | A generated chart invents data |

## 6. Failure patterns

| Pattern | Sign | Counter-move |
| --- | --- | --- |
| Generate by reflex | Credits spent on a texture code could make | License, then code, then generate |
| Invented reality | Generated "team photos" or "our office" | Real photos or none |
| Stock look by generation | A generated image that looks like the most common stock photo | Derive the image from the direction, not from the category |
| Chart as picture | A generated infographic with invented numbers | Code with real data |
| Hidden cost | Ten rounds of generation never quoted together | State the likely rounds and total up front |
| Uniqueness without a reason | Generated art where a licensed photo fit perfectly | Generate only when uniqueness matters to the brief |

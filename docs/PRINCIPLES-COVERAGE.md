# Principles coverage

This audit shows that each of the twelve books was read and integrated into the principles canon. For every book it lists the chapters from the table of contents and the principle ids drawn from each. A chapter that yields no principle carries a "Not used, and why" line.

The canon is [kit/canon/principles.json](../kit/canon/principles.json). The `design-principles` skill reads it with `scripts/principles.py`. Each book also has a readable list in `kit/canon/principles/`.

## Summary

| Book | Book id | Prefix | Chapters | Used | Principles | Gates |
| --- | --- | --- | --- | --- | --- | --- |
| [Design Systems Handbook (InVision DesignBetter)](../kit/canon/principles/design-systems-handbook.md) | `design-systems-handbook` | `P-DSH` | 7 | 6 | 32 | 14 |
| [Design Engineering Handbook (InVision DesignBetter)](../kit/canon/principles/design-engineering-handbook.md) | `design-engineering-handbook` | `P-DEH` | 6 | 6 | 29 | 6 |
| [Animation Handbook (InVision DesignBetter)](../kit/canon/principles/animation-handbook.md) | `animation-handbook` | `P-ANI` | 4 | 4 | 32 | 7 |
| [Design Collaboration Handbook (Design Better)](../kit/canon/principles/collaboration-handbook.md) | `collaboration-handbook` | `P-COL` | 7 | 7 | 31 | 7 |
| [Principles of Product Design (InVision DesignBetter)](../kit/canon/principles/principles-of-product-design.md) | `principles-of-product-design` | `P-PPD` | 7 | 7 | 39 | 10 |
| [Design Leadership Handbook (InVision DesignBetter)](../kit/canon/principles/design-leadership-handbook.md) | `design-leadership-handbook` | `P-LEAD` | 6 | 6 | 28 | 2 |
| [DesignOps Handbook (InVision DesignBetter)](../kit/canon/principles/designops-handbook.md) | `designops-handbook` | `P-OPS` | 5 | 5 | 22 | 6 |
| [Design Thinking Handbook (Design Better)](../kit/canon/principles/design-thinking-handbook.md) | `design-thinking-handbook` | `P-DT` | 6 | 6 | 32 | 6 |
| [Designing for Emotion, second edition (A Book Apart)](../kit/canon/principles/designing-for-emotion.md) | `designing-for-emotion` | `P-EMO` | 9 | 7 | 37 | 11 |
| [Mastering Gephi Network Visualization (Packt, 2015)](../kit/canon/principles/mastering-gephi.md) | `mastering-gephi` | `P-GEPHI` | 11 | 10 | 28 | 11 |
| [Build an AI app in 5 steps (Redis whitepaper, 2025)](../kit/canon/principles/ai-app-5-steps.md) | `ai-app-5-steps` | `P-AIAPP` | 7 | 7 | 8 | 0 |
| [Mapping to MCPs in Claude Cowork and Claude Code (field guide, v1.0, 2026)](../kit/canon/principles/mapping-to-mcps.md) | `mapping-to-mcps` | `P-MCP` | 6 | 5 | 7 | 2 |
| Total | | | | | 325 | 82 |

Weight follows relevance to design work: the nine handbooks carry most principles, the Gephi book carries its tool-independent network rules and skips menu steps, and the two short guides carry a few each.

## Design Systems Handbook (InVision DesignBetter)

Book id `design-systems-handbook`. List: [design-systems-handbook.md](../kit/canon/principles/design-systems-handbook.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Introducing design systems | P-DSH-01, P-DSH-02, P-DSH-03, P-DSH-04 |
| Chapter 2: Designing your design system | P-DSH-05, P-DSH-06, P-DSH-07, P-DSH-08, P-DSH-09, P-DSH-10, P-DSH-11, P-DSH-12, P-DSH-13, P-DSH-14, P-DSH-15, P-DSH-16, P-DSH-17, P-DSH-18, P-DSH-19, P-DSH-20 |
| Chapter 3: Building your design system | P-DSH-21, P-DSH-22, P-DSH-23, P-DSH-24, P-DSH-25, P-DSH-26 |
| Chapter 4: Putting your design system into practice | P-DSH-27, P-DSH-28, P-DSH-29 |
| Chapter 5: Expanding your design system | P-DSH-30, P-DSH-31 |
| Chapter 6: The future of design systems | P-DSH-32 |
| Chapter 7: Appendix | Not used, and why: A list of example systems and author biographies; it states no method. |

## Design Engineering Handbook (InVision DesignBetter)

Book id `design-engineering-handbook`. List: [design-engineering-handbook.md](../kit/canon/principles/design-engineering-handbook.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Introducing design engineering | P-DEH-01 |
| Chapter 2: The design engineering process | P-DEH-02, P-DEH-03, P-DEH-04, P-DEH-05, P-DEH-06, P-DEH-07, P-DEH-08, P-DEH-09, P-DEH-10, P-DEH-11, P-DEH-12, P-DEH-13, P-DEH-14, P-DEH-15, P-DEH-16, P-DEH-17, P-DEH-18 |
| Chapter 3: Engineering collaboration | P-DEH-19, P-DEH-20, P-DEH-21, P-DEH-22 |
| Chapter 4: Design engineering organizational models | P-DEH-23 |
| Chapter 5: Design engineering leadership | P-DEH-24, P-DEH-25, P-DEH-26, P-DEH-27 |
| Chapter 6: A design engineering manifesto | P-DEH-28, P-DEH-29 |

## Animation Handbook (InVision DesignBetter)

Book id `animation-handbook`. List: [animation-handbook.md](../kit/canon/principles/animation-handbook.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Motion's purpose | P-ANI-01, P-ANI-02, P-ANI-03, P-ANI-04, P-ANI-05, P-ANI-06, P-ANI-07, P-ANI-08 |
| Chapter 2: Principles of animation | P-ANI-09, P-ANI-10, P-ANI-11, P-ANI-12, P-ANI-13, P-ANI-14, P-ANI-15, P-ANI-16, P-ANI-17, P-ANI-18, P-ANI-19 |
| Chapter 3: Animation collaboration | P-ANI-20, P-ANI-21, P-ANI-22, P-ANI-23, P-ANI-24, P-ANI-25, P-ANI-26, P-ANI-27 |
| Chapter 4: Taking animation further | P-ANI-28, P-ANI-29, P-ANI-30, P-ANI-31, P-ANI-32 |

## Design Collaboration Handbook (Design Better)

Book id `collaboration-handbook`. List: [collaboration-handbook.md](../kit/canon/principles/collaboration-handbook.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Raising your collaborative intelligence | P-COL-01 |
| Chapter 2: Collaborative leadership | P-COL-02, P-COL-03, P-COL-04, P-COL-05, P-COL-06, P-COL-07 |
| Chapter 3: Understanding your colleagues | P-COL-08, P-COL-09, P-COL-10, P-COL-11 |
| Chapter 4: Understanding your customers | P-COL-12, P-COL-13, P-COL-14, P-COL-15 |
| Chapter 5: Mission, vision, and purpose | P-COL-16, P-COL-17, P-COL-18, P-COL-19 |
| Chapter 6: Creativity, innovation, and divergent thinking | P-COL-20, P-COL-21, P-COL-22, P-COL-23, P-COL-24, P-COL-25 |
| Chapter 7: Building together | P-COL-26, P-COL-27, P-COL-28, P-COL-29, P-COL-30, P-COL-31 |

## Principles of Product Design (InVision DesignBetter)

Book id `principles-of-product-design`. List: [principles-of-product-design.md](../kit/canon/principles/principles-of-product-design.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Guess less | P-PPD-01, P-PPD-02, P-PPD-03, P-PPD-04, P-PPD-05 |
| Chapter 2: Story first | P-PPD-06, P-PPD-07, P-PPD-08, P-PPD-09, P-PPD-10, P-PPD-11, P-PPD-12 |
| Chapter 3: Pencils before pixels | P-PPD-13, P-PPD-14, P-PPD-15, P-PPD-16, P-PPD-17 |
| Chapter 4: Show and tell | P-PPD-18, P-PPD-19, P-PPD-20, P-PPD-21, P-PPD-22, P-PPD-23, P-PPD-24, P-PPD-25, P-PPD-26 |
| Chapter 5: Fast feedback | P-PPD-27, P-PPD-28, P-PPD-29, P-PPD-30, P-PPD-31, P-PPD-32, P-PPD-33 |
| Chapter 6: Lateral design | P-PPD-34, P-PPD-35, P-PPD-36, P-PPD-37 |
| Chapter 7: Break the black box | P-PPD-38, P-PPD-39 |

## Design Leadership Handbook (InVision DesignBetter)

Book id `design-leadership-handbook`. List: [design-leadership-handbook.md](../kit/canon/principles/design-leadership-handbook.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Becoming a design leader | P-LEAD-01, P-LEAD-02, P-LEAD-03 |
| Chapter 2: Building the team | P-LEAD-04, P-LEAD-05, P-LEAD-06, P-LEAD-07, P-LEAD-08, P-LEAD-09, P-LEAD-10, P-LEAD-11, P-LEAD-12, P-LEAD-13 |
| Chapter 3: Managing a design team | P-LEAD-14, P-LEAD-15, P-LEAD-16, P-LEAD-17, P-LEAD-18 |
| Chapter 4: Operationalizing design | P-LEAD-19, P-LEAD-20, P-LEAD-21 |
| Chapter 5: Forging alliances | P-LEAD-22, P-LEAD-23 |
| Chapter 6: Shaping design vision | P-LEAD-24, P-LEAD-25, P-LEAD-26, P-LEAD-27, P-LEAD-28 |

## DesignOps Handbook (InVision DesignBetter)

Book id `designops-handbook`. List: [designops-handbook.md](../kit/canon/principles/designops-handbook.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Introducing DesignOps | P-OPS-01, P-OPS-02, P-OPS-03, P-OPS-04 |
| Chapter 2: DesignOps scenarios and models | P-OPS-05, P-OPS-06, P-OPS-07, P-OPS-08, P-OPS-09, P-OPS-10, P-OPS-11, P-OPS-12 |
| Chapter 3: Putting DesignOps into play | P-OPS-13, P-OPS-14, P-OPS-15, P-OPS-16 |
| Chapter 4: Team coordination | P-OPS-17, P-OPS-18 |
| Chapter 5: ResearchOps | P-OPS-19, P-OPS-20, P-OPS-21, P-OPS-22 |

## Design Thinking Handbook (Design Better)

Book id `design-thinking-handbook`. List: [design-thinking-handbook.md](../kit/canon/principles/design-thinking-handbook.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Why we need design thinking | P-DT-01, P-DT-02, P-DT-03 |
| Chapter 2: Empathize | P-DT-04, P-DT-05, P-DT-06, P-DT-07, P-DT-08, P-DT-09 |
| Chapter 3: Define | P-DT-10, P-DT-11, P-DT-12, P-DT-13, P-DT-14, P-DT-15 |
| Chapter 4: Ideate | P-DT-16, P-DT-17, P-DT-18, P-DT-19, P-DT-20, P-DT-21, P-DT-22 |
| Chapter 5: Prototype | P-DT-23, P-DT-24, P-DT-25, P-DT-26, P-DT-27, P-DT-28 |
| Chapter 6: Test | P-DT-29, P-DT-30, P-DT-31, P-DT-32 |

## Designing for Emotion, second edition (A Book Apart)

Book id `designing-for-emotion`. List: [designing-for-emotion.md](../kit/canon/principles/designing-for-emotion.md).

| Chapter | Principle ids |
| --- | --- |
| Chapter 1: Emotional design | P-EMO-01, P-EMO-02, P-EMO-03, P-EMO-04, P-EMO-05, P-EMO-06, P-EMO-07 |
| Chapter 2: Design for humans | P-EMO-08, P-EMO-09, P-EMO-10, P-EMO-11, P-EMO-12, P-EMO-13, P-EMO-14, P-EMO-15 |
| Chapter 3: Personality | P-EMO-16, P-EMO-17, P-EMO-18, P-EMO-19, P-EMO-20, P-EMO-21, P-EMO-22, P-EMO-23, P-EMO-24 |
| Chapter 4: Empathy and inclusion | P-EMO-25, P-EMO-26, P-EMO-27 |
| Chapter 5: Emotional engagement | P-EMO-28, P-EMO-29, P-EMO-30, P-EMO-31 |
| Chapter 6: Trust, fear, and forgiveness | P-EMO-32, P-EMO-33, P-EMO-34, P-EMO-35 |
| Chapter 7: The business of emotional design | P-EMO-36, P-EMO-37 |
| Conclusion | Not used, and why: A short closing argument that restates the earlier chapters; it adds no new method. |
| Resources | Not used, and why: A reading list and links; titles only, not read. |

## Mastering Gephi Network Visualization (Packt, 2015)

Book id `mastering-gephi`. List: [mastering-gephi.md](../kit/canon/principles/mastering-gephi.md).

| Chapter | Principle ids |
| --- | --- |
| Preface | Not used, and why: Describes the book's audience and conventions; it states no method. |
| Chapter 1: Fundamentals of complex networks and Gephi | P-GEPHI-01, P-GEPHI-02, P-GEPHI-03 |
| Chapter 2: A network graph framework | P-GEPHI-04, P-GEPHI-05, P-GEPHI-06 |
| Chapter 3: Selecting the layout | P-GEPHI-07, P-GEPHI-08, P-GEPHI-09, P-GEPHI-10, P-GEPHI-11, P-GEPHI-12 |
| Chapter 4: Network patterns | P-GEPHI-13, P-GEPHI-14 |
| Chapter 5: Working with filters | P-GEPHI-15, P-GEPHI-16 |
| Chapter 6: Graph statistics | P-GEPHI-17, P-GEPHI-18 |
| Chapter 7: Segmenting and partitioning a graph | P-GEPHI-19, P-GEPHI-20, P-GEPHI-21, P-GEPHI-22 |
| Chapter 8: Dynamic networks | P-GEPHI-23, P-GEPHI-24 |
| Chapter 9: Taking your graph beyond Gephi | P-GEPHI-25, P-GEPHI-26, P-GEPHI-27 |
| Chapter 10: Putting it all together | P-GEPHI-28 |

## Build an AI app in 5 steps (Redis whitepaper, 2025)

Book id `ai-app-5-steps`. List: [ai-app-5-steps.md](../kit/canon/principles/ai-app-5-steps.md).

| Chapter | Principle ids |
| --- | --- |
| Introduction | P-AIAPP-01 |
| Step 1: Add fast LLM memory | P-AIAPP-02 |
| Step 2: Speed up responses with semantic caching | P-AIAPP-03, P-AIAPP-04 |
| Step 3: Add agentic memory | P-AIAPP-05 |
| Step 4: Keep your app safe with rate limiting | P-AIAPP-06 |
| Step 5: Speed up ML predictions with a feature store | P-AIAPP-07 |
| Final thoughts and what to build next | P-AIAPP-08 |

## Mapping to MCPs in Claude Cowork and Claude Code (field guide, v1.0, 2026)

Book id `mapping-to-mcps`. List: [mapping-to-mcps.md](../kit/canon/principles/mapping-to-mcps.md).

| Chapter | Principle ids |
| --- | --- |
| Section 01: The basics | P-MCP-01 |
| Section 02: What ships inside | P-MCP-02, P-MCP-03 |
| Section 03: On your machine | P-MCP-04 |
| Section 04: Connecting | P-MCP-05 |
| Section 05: Adding your own | P-MCP-06, P-MCP-07 |
| Quick reference | Not used, and why: A one-page summary of sections 01 to 05; its commands are covered by the principles drawn from those sections. |

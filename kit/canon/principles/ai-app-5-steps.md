# Build an AI app in 5 steps (Redis whitepaper, 2025)

Book id `ai-app-5-steps`, id prefix `P-AIAPP`. 8 principles, 0 of them gates. The machine-readable copy is in [principles.json](../principles.json); this file matches it word for word.

Gates: none.
Every other principle is a default. Query them with the `design-principles` skill.

## Introduction

**P-AIAPP-01 Name the AI app archetype.** Before designing, classify the product as an AI app or not and, if it is one, name its archetype: assistant with memory, autonomous agent or real-time prediction system. Test: The brief of an AI product names its archetype.

## Step 1: Add fast LLM memory

**P-AIAPP-02 Memory the user can see.** Design an AI product so the end user never repeats a standing instruction and can see and edit what it remembers about them. Test: The design includes a place to view and change stored preferences.

## Step 2: Speed up responses with semantic caching

**P-AIAPP-03 Design fast and slow answers.** Design two answer speeds, near-instant and slow, and mark which answers must never be reused from a cache. Test: The state sheet shows both speeds and lists the answer types that bypass reuse.

**P-AIAPP-04 Vendor numbers are claims.** Treat performance and cost figures from a vendor document as claims until the project measures its own. Test: No gate or decision cites a vendor figure without a project measurement.

## Step 3: Add agentic memory

**P-AIAPP-05 Route by task, not habit.** Route each request to the best-fit resource, such as a general model, a specialized model, search or an outside service, from a catalog with use-when lines. Test: Each routed tool call in the plan cites the catalog's use-when line it matches.

## Step 4: Keep your app safe with rate limiting

**P-AIAPP-06 Rate limits are a designed state.** Design the usage-limit message as a first-class state that says what happened, when access returns and, for tiered plans, the remaining allowance. Test: Every AI interaction has a designed limited state with recovery information.

## Step 5: Speed up ML predictions with a feature store

**P-AIAPP-07 Show how fresh numbers are.** Show the age of every live or predicted number on a real-time dashboard. Test: Each live metric on the dashboard shows its freshness.

## Final thoughts and what to build next

**P-AIAPP-08 Hand off runtime behavior.** Hand off an AI interaction with a runtime-behavior sheet covering waiting, fast answer, slow answer, limited and failed or fallback states, not only screens. Test: The handoff for each AI interaction lists all five states with designed screens or copy.

Sources: Build an AI app in 5 steps (Redis whitepaper, 2025); Introduction, Step 1: Add fast LLM memory, Step 2: Speed up responses with semantic caching, Step 3: Add agentic memory, Step 4: Keep your app safe with rate limiting, Step 5: Speed up ML predictions with a feature store, Final thoughts and what to build next. Paraphrased in the kit's own words; no sentence is quoted.

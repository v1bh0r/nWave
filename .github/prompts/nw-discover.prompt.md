---
description: "Conducts evidence-based product discovery through customer interviews and assumption testing. Use at project start to validate problem-solution fit before writing any code."
---

# NW-DISCOVER: Evidence-Based Product Discovery

**Wave**: DISCOVER (wave 1 of 6)

Invoke `#agent:nw-product-discoverer` to execute the DISCOVER wave.

## Usage

```
/nw-discover [product-concept]
```

## What the Agent Produces

- `docs/feature/{feature-id}/discover/problem-validation.md` — evidence of problem existence
- `docs/feature/{feature-id}/discover/interview-log.md` — customer interview synthesis (Mom Test format)
- `docs/feature/{feature-id}/discover/assumption-map.md` — ranked assumptions by risk
- `docs/feature/{feature-id}/discover/market-context.md` — competitive and market analysis
- `docs/feature/{feature-id}/discover/wave-decisions.md` — summary for downstream waves

## Context Files

Provide if available (optional):
- `docs/project-brief.md` — initial product vision
- `docs/market-context.md` — market research and competitive landscape

## 4-Phase Discovery with Gates

The agent runs 4 phases with explicit gates:

| Phase | Gate |
|-------|------|
| G1: Problem Framing | Evidence of problem existence in real customers |
| G2: Assumption Mapping | All risks ranked, top 3 identified |
| G3: Customer Conversations | 5+ conversations using Mom Test principles |
| G4: Synthesis | Pivot/persevere decision based on evidence |

## Mom Test Principles (enforced)

- Ask about past behavior, not hypothetical future behavior
- Talk about customer's life, not your idea
- Future-intent statements ("I would use that") are rejected as evidence

After completion, invoke `#agent:nw-product-discoverer-reviewer` for peer review.

## Next Wave

After DISCOVER: `/nw-discuss` to define requirements and user stories.

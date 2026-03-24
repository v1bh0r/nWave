---
description: "Conducts Jobs-to-be-Done analysis, UX journey design, and requirements gathering. Use when starting feature analysis, defining user stories, or creating acceptance criteria."
---

# NW-DISCUSS: Jobs-to-be-Done Analysis and Requirements Gathering

**Wave**: DISCUSS (wave 2 of 6)

Invoke `#agent:nw-product-owner` to execute the DISCUSS wave.

## Usage

```
/nw-discuss [feature-name]
```

## Prior Wave Consultation

Before beginning DISCUSS work, read prior wave artifacts:

1. **DISCOVER** (synthesis check): Read `docs/feature/{feature-id}/discover/wave-decisions.md`. If DISCOVER was not run, proceed with available context.

Then check: does any DISCUSS direction contradict DISCOVER findings? Flag and resolve with user.

## What the Agent Produces

- `docs/feature/{feature-id}/discuss/requirements.md` — functional requirements
- `docs/feature/{feature-id}/discuss/user-stories.md` — DoR-validated user stories
- `docs/feature/{feature-id}/discuss/acceptance-criteria.md` — testable criteria
- `docs/feature/{feature-id}/discuss/story-map.md` — walking skeleton and release slicing
- `docs/feature/{feature-id}/discuss/outcome-kpis.md` — measurable success metrics
- `docs/feature/{feature-id}/discuss/wave-decisions.md` — summary for downstream waves

## Interactive Decisions

The agent will ask:
1. **Feature type**: user-facing / backend / infrastructure / cross-cutting
2. **Walking skeleton**: Yes (recommended for greenfield) / Depends / No
3. **UX research depth**: Lightweight / Comprehensive / Deep-dive
4. **JTBD analysis**: Yes (when motivations are unclear) / No

For greenfield projects (no `src/` code, no `docs/feature/` history), Luna proposes Walking Skeleton as Feature 0.

## Quality Gate: Definition of Ready (DoR)

Every user story must satisfy 9 DoR criteria before DISCUSS is complete. The agent validates each story before handoff.

After completion, invoke `#agent:nw-product-owner-reviewer` for peer review.

## Next Wave

After DISCUSS: `/nw-design` to design architecture, or `/nw-devops` for infrastructure-first features.

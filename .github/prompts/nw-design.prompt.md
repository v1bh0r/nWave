---
description: "Designs system architecture with C4 diagrams and technology selection. Use when defining component boundaries, choosing tech stacks, or creating architecture documents."
---

# NW-DESIGN: Architecture Design

**Wave**: DESIGN (wave 3 of 6)

Invoke `#agent:nw-solution-architect` to execute the DESIGN wave.

## Usage

```
/nw-design [component-name]
```

## Prior Wave Consultation

Before beginning DESIGN work, read these artifacts:

1. **DISCUSS** (primary input): Read from `docs/feature/{feature-id}/discuss/`:
   - `wave-decisions.md` — decision summary
   - `requirements.md` — functional requirements
   - `acceptance-criteria.md` — testable criteria driving architecture
   - `user-stories.md` — scope of what to build
   - `outcome-kpis.md` — quality attributes informing architecture

2. **DISCOVER** (synthesis check): Read `docs/feature/{feature-id}/discover/wave-decisions.md` if architectural decisions may be affected.

After reading, check whether any DESIGN decisions would contradict DISCUSS requirements. Flag contradictions and resolve with user before proceeding.

## What the Agent Produces

- `docs/feature/{feature-id}/design/architecture-design.md` — with C4 diagrams (Mermaid)
- `docs/feature/{feature-id}/design/component-boundaries.md` — dependency-inversion boundaries
- `docs/feature/{feature-id}/design/technology-stack.md` — technology decisions with rationale
- `docs/feature/{feature-id}/design/adr/` — Architecture Decision Records for significant choices
- `docs/feature/{feature-id}/design/wave-decisions.md` — downstream wave summary

## Quality-Attribute-Driven Approach

The agent drives architecture from quality attributes, not pattern shopping:
1. Understand what JTBD the architecture must serve (from DISCUSS)
2. Identify constraints: team size, timeline, existing systems, regulatory requirements
3. Map quality attributes: scalability, maintainability, testability, fault tolerance, auditability
4. Select patterns that fit (monolith → microservices → event-driven → CQRS → etc.)

After completion, invoke `#agent:nw-solution-architect-reviewer` for peer review.

## Next Wave

After DESIGN: `/nw-devops` to design platform readiness, then `/nw-distill` for acceptance tests.

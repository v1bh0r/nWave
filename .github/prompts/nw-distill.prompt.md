---
description: "Creates E2E acceptance tests in Given-When-Then format from requirements and architecture. Use when preparing executable specifications before implementation."
---

# NW-DISTILL: Acceptance Test Creation

**Wave**: DISTILL (wave 5 of 6)

Invoke `#agent:nw-acceptance-designer` to execute the DISTILL wave.

## Usage

```
/nw-distill [story-id]
```

## Prior Wave Consultation

Before beginning DISTILL work, read:

1. **DISCUSS** (requirements source): Read from `docs/feature/{feature-id}/discuss/`:
   - `user-stories.md` — stories to create tests for
   - `acceptance-criteria.md` — testable criteria
   - `requirements.md` — functional requirements

2. **DESIGN** (structural context): Read `docs/feature/{feature-id}/design/architecture-design.md`
   — component ports mapped to test entry points

3. **DEVOPS** (infrastructure testing): Read `docs/feature/{feature-id}/devops/deployment-strategy.md`
   — environment assumptions for acceptance test setup

## Interactive Decisions

The agent will ask:
1. **Feature scope**: Core feature / Extension / Bug fix
2. **Test framework**: pytest-bdd / Cucumber / SpecFlow / Custom
3. **Integration approach**: Real services / Test containers / Mocks for external only
4. **Infrastructure testing**: Include CI/CD validation smoke tests? Yes / No

## What the Agent Produces

- `docs/feature/{feature-id}/distill/acceptance-tests/` — Given-When-Then test files
- `docs/feature/{feature-id}/distill/test-scenarios.md` — scenario summary with port mapping
- `docs/feature/{feature-id}/distill/wave-decisions.md` — summary for DELIVER wave

## Port-to-Port Principle

Every acceptance criterion names the driving port (entry point):
- Observable outcome: what the user/system sees
- Driving port: the entry point that triggers the behavior (endpoint, handler, CLI command)

This makes TBU (Tested But Unwired) defects structurally impossible.

After completion, invoke `#agent:nw-acceptance-designer-reviewer` for peer review.

## Next Wave

After DISTILL: `/nw-deliver` to implement via Outside-In TDD using these acceptance tests as the outer RED.

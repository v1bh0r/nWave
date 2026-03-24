---
description: "Orchestrates the full DELIVER wave end-to-end (roadmap → execute all steps → finalize). Use when all prior waves are complete and the feature is ready for implementation."
---

# NW-DELIVER: Complete DELIVER Wave Orchestrator

**Wave**: DELIVER (wave 6 of 6)

Invoke `#agent:nw-software-crafter` (default) or `#agent:nw-functional-software-crafter` for FP paradigm projects.

## Usage

```
/nw-deliver "Implement user authentication with JWT"
```

## Prior Wave Consultation

Before beginning DELIVER work, read targeted prior wave artifacts.

1. **DESIGN** (structural context): Read from `docs/feature/{feature-id}/design/`:
   - `architecture-design.md` — component structure and C4 diagrams
   - `component-boundaries.md` — dependency-inversion boundaries

2. **DISTILL** (primary input): Read from `docs/feature/{feature-id}/distill/`:
   - `acceptance-tests/` — all Given-When-Then acceptance tests
   - Each acceptance test encodes all prior wave decisions

3. **Roadmap**: Read `docs/feature/{feature-id}/deliver/roadmap.json`.
   If no roadmap exists, use `/nw-roadmap` first.

## Paradigm Selection

Detect FP vs OOP:
- FP indicators: functional language (F#, Haskell, Scala, Clojure, Elixir); existing codebase uses Railway error handling or discriminated unions
- Default: OOP → `#agent:nw-software-crafter`
- FP confirmed → `#agent:nw-functional-software-crafter`

## Execution Loop

For each step in `roadmap.json` (in order):

1. Extract step context: `step_id`, `description`, `acceptance_criteria`, `files_to_modify`
2. Invoke the selected crafter agent with the step context
3. Verify the step produced a commit before proceeding to the next step
4. After all steps: invoke `#agent:nw-software-crafter-reviewer` for adversarial review

## Orchestration Mandate

You are ORCHESTRATOR — coordinate, never implement directly.
- NEVER write code or tests yourself
- NEVER write entries to `execution-log.json` — only the crafter agent may append entries
- ALL implementation delegated to the crafter agent via `#agent:` invocation

## Rigor Profile

Read `.nwave/des-config.json` (key: `rigor`) before dispatching agents. Adjust:
- `review_enabled: false` → skip adversarial review phase
- `tdd_phases: [RED_UNIT, GREEN]` → inform crafter to skip PREPARE/RED_ACCEPTANCE/COMMIT phases
- `mutation_enabled: true` → run mutation testing after all steps complete

## Success Criteria

- All steps in `roadmap.json` have `status: DONE`
- All acceptance tests pass
- No regressions in existing test suite
- `execution-log.json` contains a COMMIT entry for each step

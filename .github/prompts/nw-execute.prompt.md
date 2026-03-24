---
description: "Dispatches a single roadmap step to a specialized agent for TDD execution. Use when implementing a specific step from a roadmap.json plan."
---

# NW-EXECUTE: Atomic Task Execution

**Wave**: EXECUTE

Dispatch a single roadmap step to the specified agent.

## Usage

```
/nw-execute #agent:nw-software-crafter [feature-id] [step-id]
```

Example:
```
/nw-execute #agent:nw-software-crafter "auth-upgrade" "01-01"
```

## Execution Steps

1. Parse parameters: agent name, feature ID, step ID
2. Read rigor profile from `.nwave/des-config.json` (key: `rigor`). Default: standard.
3. Validate `docs/feature/{feature-id}/deliver/roadmap.json` exists
4. Validate `docs/feature/{feature-id}/deliver/execution-log.json` exists
5. Find step `{step-id}` in roadmap.json — extract:
   - `description`
   - `acceptance_criteria`
   - `files_to_modify`
6. Invoke the specified agent with the step context

## Agent Invocation Context

Pass to the agent:

```
Execute TDD implementation for step {step-id}:

Description: {description}

Acceptance Criteria:
{acceptance_criteria}

Files to Modify:
{files_to_modify}

TDD Phases: PREPARE → RED_ACCEPTANCE → RED_UNIT → GREEN → COMMIT

After all phases complete:
- Append step entry to docs/feature/{feature-id}/deliver/execution-log.json
- Commit with: feat({scope}): {description}
```

## Rigor Adjustments

| Rigor setting | Effect |
|---------------|--------|
| `tdd_phases: [RED_UNIT, GREEN]` | Tell agent to skip PREPARE/RED_ACCEPTANCE/COMMIT |
| `refactor_pass: false` | Tell agent to skip refactoring in COMMIT phase |

## Success Criteria

- Step has `status: DONE` in execution-log.json
- Commit exists with matching conventional commit message
- All tests pass

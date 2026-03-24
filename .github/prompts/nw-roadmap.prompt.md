---
description: "Creates a phased roadmap.json for a feature goal with acceptance criteria and TDD steps. Use when planning implementation before execution."
---

# NW-ROADMAP: Goal Planning

**Wave**: CROSS_WAVE

Dispatch an expert agent to create a structured implementation roadmap.

## Usage

```
/nw-roadmap #agent:nw-solution-architect "Migrate monolith to microservices"
/nw-roadmap #agent:nw-software-crafter "Replace legacy authentication system"
```

## Execution Steps

### Step 1: Parse Parameters

1. Agent name (after `#agent:`)
2. Goal description (quoted string)
3. Derive `feature-id`: "Migrate to OAuth2" → `migrate-to-oauth2`

### Step 2: Create Output Directory

Create: `docs/feature/{feature-id}/deliver/` if it doesn't exist.
Create empty: `docs/feature/{feature-id}/deliver/execution-log.json` with `{"steps": []}`.

### Step 3: Read Prior Wave Artifacts

Read from `docs/feature/{feature-id}/distill/acceptance-tests/` — these drive the roadmap.
Read `docs/feature/{feature-id}/design/architecture-design.md` if it exists.

### Step 4: Invoke Agent

Invoke the specified agent (e.g., `#agent:nw-solution-architect`):

```
Create a roadmap.json for: {goal-description}

Feature ID: {feature-id}
Output: docs/feature/{feature-id}/deliver/roadmap.json

Acceptance tests (use these to derive steps): {acceptance_tests_content}
Architecture context: {architecture_content}

Roadmap format:
{
  "project_id": "{feature-id}",
  "goal": "{goal-description}",
  "steps": [
    {
      "step_id": "01-01",
      "description": "...",
      "acceptance_criteria": [...],
      "files_to_modify": [...],
      "status": "pending"
    }
  ]
}

Requirements:
- Steps ordered from outside-in (acceptance test → unit test → implementation)
- Each step has 1-3 acceptance criteria mapped from the acceptance tests
- Steps are sized for a single TDD cycle (1-2 hours)
- Step IDs are sequential: 01-01, 01-02, 02-01, etc.
```

## Success Criteria

- `docs/feature/{feature-id}/deliver/roadmap.json` exists and is valid JSON
- All acceptance test scenarios have at least one corresponding step
- Steps are ordered (outer RED before inner RED before GREEN)

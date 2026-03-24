---
description: "Bug fix workflow: root cause analysis → user review → regression test + fix via TDD. Use when investigating and fixing defects."
---

# NW-BUGFIX: Defect Resolution Workflow

**Wave**: CROSS_WAVE

## Usage

```
/nw-bugfix [bug-description]
```

## Flow

```
INPUT: bug-description
  │
  ├─ Phase 1: Root Cause Analysis (#agent:nw-troubleshooter)
  │   └─ 5-Why investigation with evidence at each level
  │   └─ Output: RCA document with root cause chain + fix proposal
  │
  ├─ Phase 2: User Review (STOP — interactive)
  │   └─ Present RCA findings to user
  │   └─ User confirms root cause + approves fix direction
  │   └─ If user rejects → refine RCA or stop
  │
  └─ Phase 3: Regression Test + Fix (#agent:nw-software-crafter)
      └─ Roadmap: regression test (RED) → fix (GREEN) → verify (COMMIT)
```

## Phase 1: Root Cause Analysis

Invoke `#agent:nw-troubleshooter` with:

```
Investigate the following defect using Toyota 5-Why methodology:

{bug-description}

Requirements:
- investigation_depth: 5 (all branches must reach level 5)
- multi_causal: true (investigate all contributing factors)
- evidence_required: true (cite observable evidence at each Why-level)

Produce:
1. Root cause chain (5 Whys with evidence at each level)
2. Contributing factors
3. Proposed fix with specific code changes
4. Files affected
5. Regression test description (what test would catch this bug)
```

## Phase 2: User Review

After the troubleshooter returns its RCA, summarize:
- Root cause: [single sentence]
- Fix proposed: [specific changes]
- Test that would prevent recurrence: [test description]

Ask user to confirm before proceeding to Phase 3.

## Phase 3: Regression Test + Fix

Derive a `bug-id` from the description (kebab-case). Create `docs/feature/bugfix-{bug-id}/`.

Invoke `#agent:nw-software-crafter` with:
- Write the regression test first (it must fail with the bug)
- Then implement the fix (test must pass)
- Then verify no regressions in the existing test suite
- Commit with: `fix(scope): {description}`

## Success Criteria

- Regression test exists and was red before fix
- Regression test is green after fix
- No existing tests broken
- Conventional commit produced

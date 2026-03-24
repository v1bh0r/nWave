---
description: "Archives a completed feature to docs/evolution/, migrates lasting artifacts to permanent directories, and cleans up the temporary workspace. Use after all implementation steps pass."
---

# NW-FINALIZE: Feature Completion and Archive

**Wave**: CROSS_WAVE

Invoke `#agent:nw-platform-architect` (default) or specify another agent.

## Usage

```
/nw-finalize [feature-id] [--agent=platform-architect|software-crafter]
```

## Pre-Finalize Gate: All Steps Must Be Complete

Before invoking any agent, verify all steps are `DONE`:

1. Read `docs/feature/{feature-id}/deliver/execution-log.json`
2. Check every step has `status: DONE`
3. If any step is not `DONE`, block and list incomplete steps with current status
4. Do NOT proceed until all steps are complete

## What Gets Archived vs Migrated

`docs/feature/{feature-id}/` is a **temporary workspace** — cleaned up at finalize.

| Artifact | Action |
|----------|--------|
| Architecture decisions | Migrate to `docs/architecture/` |
| ADRs | Migrate to `docs/adrs/` |
| Research documents | Migrate to `docs/research/` |
| Deployment docs | Migrate to `docs/operations/` |
| Evolution summary | Create at `docs/evolution/YYYY-MM-DD-{feature-id}.md` |
| Acceptance tests | Keep in test suite (already committed) |
| Wave working files | Discard |

## Agent Invocation

Invoke `#agent:nw-platform-architect` (or specified agent):

```
Finalize feature {feature-id}.

Completed steps: {count} (all DONE verified)
Feature directory: docs/feature/{feature-id}/
Roadmap: docs/feature/{feature-id}/deliver/roadmap.json
Execution log: docs/feature/{feature-id}/deliver/execution-log.json

1. Read execution-log.json and roadmap.json to understand what was built
2. Create evolution document at docs/evolution/YYYY-MM-DD-{feature-id}.md
3. Migrate lasting artifacts to permanent directories
4. Remove docs/feature/{feature-id}/ temporary workspace
5. Produce final commit: chore({feature-id}): finalize and archive feature
```

## Evolution Document Structure

- Feature summary and business context
- Key architectural decisions made
- Technical debt introduced (and tickets created)
- Lessons learned / retrospective findings
- Links to migrated artifacts

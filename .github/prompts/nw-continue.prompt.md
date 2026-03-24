---
description: "Detects current wave progress for a feature and resumes at the next step. Scans docs/feature/ for artifacts."
---

# NW-CONTINUE: Resume a Feature

**Wave**: CROSS_WAVE (entry point)

This wizard runs directly — no agent invocation needed.

## Usage

```
/nw-continue [feature-id]
```

## Wizard Flow

### Step 1: Scan for Projects

If `feature-id` is provided, use it directly.

Otherwise list `docs/feature/` for active project directories. If none found, suggest `/nw-new`.

### Step 2: Project Selection (Multiple Projects)

If multiple directories exist, list by most recently modified file. Ask user to select.

### Step 3: Wave Progress Detection

Check each wave's completion by scanning for expected artifacts:

| Wave | Complete if these exist |
|------|------------------------|
| DISCOVER | `discover/wave-decisions.md` |
| DISCUSS | `discuss/wave-decisions.md` + `discuss/user-stories.md` |
| DESIGN | `design/wave-decisions.md` + `design/architecture-design.md` |
| DEVOPS | `devops/wave-decisions.md` + `devops/ci-cd-pipeline.md` |
| DISTILL | `distill/wave-decisions.md` + `distill/acceptance-tests/` |
| DELIVER | `deliver/execution-log.json` with all steps `DONE` |

### Step 4: DELIVER Progress Detail

If DELIVER is in progress:
- Read `docs/feature/{id}/deliver/execution-log.json`
- Count steps with `status: DONE`
- Find first step without `DONE`
- Display: "DELIVER in progress: Steps 1-3 complete. Next: step 4"

### Step 5: Wave Anomalies

Warn if:
- Non-adjacent waves completed (skipped waves) — offer to fill the gap or continue as-is
- Artifact files are empty (0 bytes) — recommend re-running that wave

### Step 6: Resume

Launch the appropriate wave command for the next incomplete step.

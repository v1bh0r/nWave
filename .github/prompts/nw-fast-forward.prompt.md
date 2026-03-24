---
description: "Fast-forwards through remaining waves end-to-end without stopping for review between waves. Use when you want to run all waves automatically after initial confirmation."
---

# NW-FAST-FORWARD: End-to-End Wave Execution

**Wave**: CROSS_WAVE (orchestrator)

## Usage

```
/nw-fast-forward [feature-description] [--from=discuss|design|devops|distill|deliver]
```

## Behavior

Chains remaining waves end-to-end after single user confirmation. Each wave is invoked in sequence — DISCUSS → DESIGN → DEVOPS → DISTILL → DELIVER — without stopping between waves.

**DISCOVER is skipped by default** — it requires interactive customer interview data. Use `--from=discover` to include it.

## Step 1: Input Parsing

- With feature description → new project
- With `--from` flag → resume from that wave
- No arguments → auto-detect from `docs/feature/`

## Step 2: Project Resolution

**New project**: Derive feature ID in kebab-case from description. Show derived ID, allow override. Create `docs/feature/{feature-id}/`.

**Existing project**: List `docs/feature/` directories, ask user to select.

## Step 3: Detect Current Progress

Check wave artifacts (same logic as `/nw-continue`):

| Wave | Ready if |
|------|----------|
| DISCOVER | `discover/wave-decisions.md` exists |
| DISCUSS | `discuss/wave-decisions.md` exists |
| DESIGN | `design/wave-decisions.md` exists |
| DEVOPS | `devops/wave-decisions.md` exists |
| DISTILL | `distill/wave-decisions.md` exists |
| DELIVER | `deliver/execution-log.json` all steps DONE |

## Step 4: Confirm Sequence with User

Show the planned wave sequence and confirm:
"I'll run: {waves}. This will proceed automatically after each wave completes. Confirm?"

Stop if user rejects.

## Step 5: Execute Waves in Sequence

For each wave in sequence:
1. Run the wave using the appropriate prompt logic
2. Verify wave completion (check for `wave-decisions.md`)
3. Proceed to next wave

If any wave fails or cannot continue, stop and report the failure.

## Notes

- `--from` without pre-existing artifacts for prerequisite waves shows an error: "Cannot start from {wave} — {missing} artifacts missing."
- Each wave runs its peer reviewer before marking complete

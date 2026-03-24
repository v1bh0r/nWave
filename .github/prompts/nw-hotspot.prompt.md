---
description: "Git change frequency hotspot analysis — find the most-changed files in your codebase to prioritize refactoring and review effort."
---

# NW-HOTSPOT: Code Change Frequency Analysis

**Wave**: CROSS_WAVE

Runs inline — no agent invocation. Execute git commands directly.

## Usage

```
/nw-hotspot [--top=N] [--since=6m]
```

## Default Analysis

Run the following to find the most-changed files:

```bash
git log --since=6m --format=format: --name-only | sort | uniq -c | sort -rn | head -20
```

Then verify each file still exists and get its last changed date:

```bash
git log -1 --format="%ar" -- {file}
```

## Output Format

Display ranked table:

```
 Rank │ Commits │ Last Changed │ File
──────┼─────────┼──────────────┼─────────────────────────
    1 │      47 │  2 days ago  │ src/des/orchestrator.py
    2 │      31 │  5 days ago  │ tests/des/test_core.py
```

## Configuration

| Flag | Default | Description |
|------|---------|-------------|
| `--top` | 20 | Number of files to show |
| `--since` | `6m` | Time window (e.g., `3m`, `6m`, `12m`, `2y`) |

## Interpretation

**High churn + high complexity**: primary refactoring candidate (use `/nw-refactor`)
**High churn + recent changes**: review for test coverage (use `/nw-review software-crafter`)
**High churn + bugs**: investigation target (use `/nw-bugfix`)

Use as a **pre-filter** to scope refactoring or a **post-filter** to prioritize existing findings.

---
description: "Selects a quality-vs-token-consumption profile (lean, standard, thorough, exhaustive) and persists it globally or per-project. Use when tuning how much rigor wave commands apply."
---

# NW-RIGOR: Quality Profile Selection

**Wave**: CROSS_WAVE

Runs directly as a wizard — no agent invocation needed.

## Usage

```
/nw-rigor [profile] [--scope=global|project]
```

## Profile Reference

| Setting | lean | standard | thorough | exhaustive |
|---------|------|----------|----------|------------|
| Review enabled | No | Yes | Yes | Yes |
| Double review | No | No | Yes | Yes |
| TDD phases | RED_UNIT, GREEN | Full 5-phase | Full 5-phase | Full 5-phase |
| Refactor pass | No | Yes | Yes | Yes |
| Mutation testing | No | No | No | Yes |

**Recommended**: `standard` — balanced quality and efficiency.

## Modes

### Mode 1: Interactive (no argument)

Show the 4 profiles with descriptions, ask user to select.

### Mode 2: Quick Switch (profile provided)

Validate profile name is one of: `lean`, `standard`, `thorough`, `exhaustive`.

### Mode 3: Custom (argument is `custom`)

Ask for each setting individually:
- Review enabled? (yes/no)
- Double review? (yes/no)
- TDD phases? (enter comma-separated subset or "all")
- Refactor pass? (yes/no)
- Mutation testing? (yes/no)

## Scope Selection

Ask user:
1. **Project-scope** — save to `.nwave/des-config.json` (affects this project only)
2. **Global scope** — save to `~/.nwave/global-config.json` (affects all projects)

Project scope overrides global scope.

## Config File Format

```json
{
  "rigor": {
    "review_enabled": true,
    "double_review": false,
    "tdd_phases": ["PREPARE", "RED_ACCEPTANCE", "RED_UNIT", "GREEN", "COMMIT"],
    "refactor_pass": true,
    "mutation_enabled": false
  }
}
```

Write config file and confirm: "Rigor profile `{profile}` saved to `{path}`."

---
description: "Applies the Refactoring Priority Premise (RPP) levels L1-L6 for systematic code refactoring. Use when improving code quality through structured refactoring passes."
---

# NW-REFACTOR: Systematic Code Refactoring

**Wave**: CROSS_WAVE

Invoke `#agent:nw-software-crafter` to execute the refactoring.

## Usage

```
/nw-refactor [target-class-or-module] [--level=1-6] [--from=1] [--to=3] [--scope=method|class|module]
```

## RPP Level Hierarchy

| Level | Name | Focus |
|-------|------|-------|
| L1 | Readability | Naming, formatting, comments |
| L2 | Complexity | Cyclomatic complexity, method length |
| L3 | Responsibilities | Single responsibility, cohesion |
| L4 | Abstractions | Interfaces, dependency inversion |
| L5 | Design Patterns | GoF patterns, structural improvements |
| L6 | SOLID++ | Full SOLID + DRY + YAGNI review |

Default: `--from=1 --to=3` (Readability through Responsibilities).

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| `level` | 3 | Shorthand for `--from=1 --to={level}` |
| `from` | 1 | Start RPP level |
| `to` | 3 | End RPP level |
| `scope` | `module` | `file`, `module`, or `project` |
| `method` | `extract` | Primary refactoring method: `extract/inline/rename/move` |

Agent invocation context:

```
Execute *refactor for {target-class-or-module}.

Configuration:
- from: {from}
- to: {to}
- scope: {scope}
- method: {method}

Context:
- src/* — production codebase
- tests/* — test codebase

Requirements:
1. Apply RPP levels in sequence (L1 must complete before L2, etc.)
2. All tests must pass after each level
3. Measure code quality before and after
4. Commit at each RPP level with: refactor(scope): L{n} {description}
```

## Success Criteria

- Code quality metrics improved (measured before/after)
- All tests passing after refactoring
- Refactoring levels applied in correct sequence
- Separate commit per RPP level applied

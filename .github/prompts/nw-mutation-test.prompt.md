---
description: "Runs feature-scoped mutation testing to validate test suite quality. Use after implementation to verify tests catch real bugs (kill rate >= 80%)."
---

# NW-MUTATION-TEST: Feature-Scoped Mutation Testing

**Wave**: QUALITY_GATE

Invoke `#agent:nw-software-crafter` to run mutation testing.

## Usage

```
/nw-mutation-test [feature-id] [--threshold=75|80|85] [--language=auto|python|java|javascript]
```

## Pre-Invocation (Orchestrator Does This)

Before invoking the agent:

1. Read `docs/feature/{feature-id}/deliver/execution-log.json`
2. Extract implementation files from `completed_steps[].files_modified.implementation`
3. Verify all extracted files exist on disk
4. Detect project language from config files (pyproject.toml → Python, pom.xml → Java, package.json → JS/TS)
5. Confirm test suite passes: run tests first, block if any fail

For Python: verify `.venv-mutation/` with `cosmic-ray` installed. If missing, install it.

## Agent Invocation

Invoke `#agent:nw-software-crafter`:

```
Run mutation testing for feature {feature-id}.

Implementation files (extracted from execution-log.json):
{file_list}

Configuration:
- language: {language}  (python|java|javascript)
- kill_rate_threshold: {threshold}%  (default: 80)
- test_scope: tests/  (or feature-specific sub-path)
- tool: cosmic-ray (Python) | PIT (Java) | Stryker (JS/TS/C#)

Requirements:
1. Generate scoped mutation config targeting ONLY the listed files
2. Run mutations, collect surviving mutants
3. Kill rate = killed / total * 100
4. If kill rate < threshold: identify and kill top surviving mutants by writing better tests
5. Report: total mutants, killed, survived, kill rate, equivalents found
```

## Success Criteria

- Kill rate >= threshold (default 80%)
- Report produced at `docs/feature/{feature-id}/deliver/mutation-report.md`
- Any surviving mutants either killed or classified as equivalents with justification

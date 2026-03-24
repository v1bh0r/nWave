---
description: "Root cause analysis using Toyota 5 Whys methodology. Use when investigating bugs, outages, or recurring failures."
---

# NW-ROOT-WHY: Toyota 5 Whys Root Cause Analysis

**Wave**: CROSS_WAVE

Invoke `#agent:nw-troubleshooter` to investigate the problem.

## Usage

```
/nw-root-why [problem-description] [--depth=3|5|7] [--output=text|diagram|report]
```

## Agent Invocation

Invoke `#agent:nw-troubleshooter`:

```
Investigate root cause for: {problem-description}

Configuration:
- investigation_depth: 5  (all branches must reach this level)
- multi_causal: true       (explore all contributing factors)
- evidence_required: true  (cite observable evidence at each Why-level)
- output_format: {text|diagram|report}

Requirements:
1. Use Toyota 5 Whys — trace each branch to level 5
2. At each Why: state the cause AND the evidence (log, observation, measurement)
3. Identify alternative hypotheses BEFORE selecting the root cause
4. State why the selected root cause explains all observed symptoms
5. Propose specific fix with files affected

Output:
- Root cause chain (tree format if multi-causal)
- Evidence citations at each level
- Alternative hypotheses considered
- Proposed fix
- Files affected
- Regression test recommendation (what test would catch this)
```

## Output Options

| Format | Use when |
|--------|----------|
| `text` | Quick investigation, inline output |
| `diagram` | Multi-causal with multiple branches (Mermaid tree) |
| `report` | Post-mortem quality, markdown document saved to `docs/post-mortems/` |

## Usage in DELIVER Wave (Phase 3.5 Retrospective)

When invoked from `/nw-deliver` retrospective, analyze across 4 categories:
1. What worked well (preserve)
2. What worked better than before (reinforce)
3. What worked badly (5 Whys, actionable fix)
4. What worked worse than before (prevent regression)

Tag framework improvements as **meta-improvements**.

After completion, invoke `#agent:nw-troubleshooter-reviewer` for peer review.

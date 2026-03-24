---
description: "Dispatches an expert reviewer agent to critique workflow artifacts. Use when a roadmap, implementation, design, or any wave artifact needs quality review."
---

# NW-REVIEW: Expert Critique and Quality Assurance

**Wave**: CROSS_WAVE

## Usage

```
/nw-review [agent-type] [artifact-path]
```

Examples:
```
/nw-review software-crafter "docs/feature/auth/deliver/roadmap.json"
/nw-review acceptance-designer "docs/feature/auth/distill/acceptance-tests/"
/nw-review solution-architect "docs/feature/auth/design/architecture-design.md"
```

## Reviewer Routing

Append `-reviewer` to the agent type to get the reviewer:

| Agent type | Reviewer invoked |
|------------|-----------------|
| `software-crafter` | `#agent:nw-software-crafter-reviewer` |
| `acceptance-designer` | `#agent:nw-acceptance-designer-reviewer` |
| `solution-architect` | `#agent:nw-solution-architect-reviewer` |
| `platform-architect` | `#agent:nw-platform-architect-reviewer` |
| `product-owner` | `#agent:nw-product-owner-reviewer` |
| `product-discoverer` | `#agent:nw-product-discoverer-reviewer` |
| `documentarist` | `#agent:nw-documentarist-reviewer` |
| `researcher` | `#agent:nw-researcher-reviewer` |
| `troubleshooter` | `#agent:nw-troubleshooter-reviewer` |
| `data-engineer` | `#agent:nw-data-engineer-reviewer` |
| `agent-builder` | `#agent:nw-agent-builder-reviewer` |

## Review Philosophy: Radical Candor

Every review embodies Radical Candor — kind AND clear, specific AND sincere:
- Acknowledge what works before critiquing
- Be specific about what is wrong and WHY
- Never "LGTM" when real issues exist
- Focus on work, not author

## Feedback Format: Conventional Comments

All findings use Conventional Comments labels:

| Label | Blocking? |
|-------|-----------|
| `praise:` | No |
| `issue (blocking):` | Yes |
| `issue (blocking, security):` | Yes — maximum directness |
| `suggestion (non-blocking):` | No |
| `nitpick (non-blocking):` | No |

## Approval Criteria

| Verdict | Criteria |
|---------|----------|
| **APPROVED** | No blocking issues |
| **NEEDS_REVISION** | Blocking issues exist — each enumerated |
| **REJECTED** | Fundamental design problems requiring significant rework |

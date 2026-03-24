---
description: "Gathers knowledge from web and files, cross-references multiple sources, and produces cited research documents. Use when investigating technologies, patterns, or decisions that need evidence backing."
---

# NW-RESEARCH: Evidence-Driven Knowledge Research

**Wave**: CROSS_WAVE

Invoke `#agent:nw-researcher` to execute the research task.

## Usage

```
/nw-research [topic] [--research_depth=overview|detailed|comprehensive|deep-dive] [--skill-for=agent-name]
```

## Configuration

| Parameter | Default | Options |
|-----------|---------|---------|
| `research_depth` | `detailed` | `overview`, `detailed`, `comprehensive`, `deep-dive` |
| `--skill-for` | (none) | agent name — distills research into a practitioner skill file |

## What the Agent Produces

- `docs/research/{topic-slug}.md` — cited research document with source tiers
- Optional: `nWave/skills/{agent-name}/SKILL.md` — practitioner-focused skill file (if `--skill-for` provided)

## Trusted Source Config

Before invoking, check for `.nwave/trusted-source-domains.yaml`. If missing, the agent seeds it with defaults (academic, official docs, industry sources) and notifies you.

## Progressive Writing Mandate

The agent creates the output file in the first 5 turns with a skeleton. All subsequent findings are written directly to the file as gathered — never held only in context. If interrupted, the file contains all work done so far.

## Research Depth Guide

- `overview` — 3-5 key findings, 10-15 sources, ~2,000 words
- `detailed` — comprehensive analysis, 20-30 sources, ~4,000 words
- `comprehensive` — exhaustive coverage, 40+ sources, ~8,000 words
- `deep-dive` — maximum depth with academic rigor, all source tiers

After completion, invoke `#agent:nw-researcher-reviewer` for peer review.

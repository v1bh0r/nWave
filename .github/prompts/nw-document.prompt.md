---
description: "Creates evidence-based documentation following DIVIO/Diataxis principles. Use when writing tutorials, how-to guides, reference docs, or explanations."
---

# NW-DOCUMENT: DIVIO Documentation Creation

**Wave**: CROSS_WAVE

Orchestrates research and documentation writing with peer review at each gate.

## Usage

```
/nw-document [topic] [--type=tutorial|howto|reference|explanation] [--research-depth=overview|detailed|comprehensive|deep-dive]
```

If `--type` is omitted, ask the user which documentation type they need.

Auto-select `research-depth` based on type if omitted:
- `tutorial` → `overview`
- `howto` → `detailed`
- `reference` → `comprehensive`
- `explanation` → `deep-dive`

## Orchestration Pipeline

```
Phase 1: Research           #agent:nw-researcher
Phase 1.5: Research Review  #agent:nw-researcher-reviewer
Phase 2: Documentation      #agent:nw-documentarist
Phase 2.5: Doc Review       #agent:nw-documentarist-reviewer
```

## DIVIO Document Types

| Type | Purpose | Example |
|------|---------|---------|
| Tutorial | Learning-oriented step-by-step | "Getting started with nWave" |
| How-to Guide | Task-oriented, assumes skill | "How to configure trusted sources" |
| Reference | Information-oriented, comprehensive | "Agent frontmatter schema" |
| Explanation | Understanding-oriented, big picture | "Why nWave uses 5-phase TDD" |

## Phase 1: Research

Invoke `#agent:nw-researcher`:
```
Research {topic} to inform {type} documentation.
research_depth: {depth}
output_directory: docs/research/
```

After researcher completes, invoke `#agent:nw-researcher-reviewer` on the research output. If NEEDS_REVISION, request one revision before proceeding.

## Phase 2: Documentation

Invoke `#agent:nw-documentarist`:
```
Create {type} documentation for {topic}.
Base it on: docs/research/{topic-slug}.md
DIVIO type: {type}
Output: docs/{type}s/{topic-slug}.md
Follow DIVIO type purity rules (80%+ from one quadrant).
```

After documentarist completes, invoke `#agent:nw-documentarist-reviewer`. If NEEDS_REVISION, request one revision.

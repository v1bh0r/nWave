---
description: "Generates C4 architecture diagrams (context, container, component) in Mermaid or PlantUML format."
---

# NW-DIAGRAM: Architecture Diagram Generation

**Wave**: CROSS_WAVE

Invoke `#agent:nw-solution-architect` to generate diagrams.

## Usage

```
/nw-diagram [diagram-type] [--format=mermaid|plantuml] [--level=context|container|component]
```

## Context Files Required

Ensure these exist before running:
- `docs/architecture/architecture-design.md`
- `docs/architecture/component-boundaries.md`
- `docs/architecture/technology-stack.md`

## Configuration

| Parameter | Default | Options |
|-----------|---------|---------|
| `diagram-type` | `component` | `component`, `deployment`, `sequence`, `data`, `context` |
| `format` | `mermaid` | `mermaid`, `plantuml`, `c4` |
| `level` | `container` | `context`, `container`, `component` |

Agent invocation:

```
Read the architecture documents:
- docs/architecture/architecture-design.md
- docs/architecture/component-boundaries.md
- docs/architecture/technology-stack.md

Generate {diagram-type} diagram in {format} format at {level} level.

Requirements:
- Diagrams must render without syntax errors
- Use audience-appropriate detail: high-level context for stakeholders, component details for developers
- Output to: docs/architecture/diagrams/{diagram-type}-{level}.{format}.md

## Success Criteria

- Diagrams accurately represent current architecture
- All diagrams render without syntax errors
- Saved to `docs/architecture/diagrams/`

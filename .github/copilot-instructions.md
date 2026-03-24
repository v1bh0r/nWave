# nWave — AI Workflow Framework for GitHub Copilot

nWave is a wave-based software development methodology that routes every task through specialized agents in a disciplined sequence, enforcing TDD, BDD, and structured quality gates.

## Wave Sequence

```
DISCOVER → DISCUSS → DESIGN → DEVOPS → DISTILL → DELIVER
```

| Wave | Command | Agent | Output |
|------|---------|-------|--------|
| DISCOVER | `/nw-discover` | `nw-product-discoverer` | Evidence, opportunity validation |
| DISCUSS | `/nw-discuss` | `nw-product-owner` | User stories, acceptance criteria |
| DESIGN | `/nw-design` | `nw-solution-architect` | Architecture, ADRs, C4 diagrams |
| DEVOPS | `/nw-devops` | `nw-platform-architect` | CI/CD, infrastructure, observability |
| DISTILL | `/nw-distill` | `nw-acceptance-designer` | BDD acceptance tests (Given-When-Then) |
| DELIVER | `/nw-deliver` | `nw-software-crafter` | Working code via Outside-In TDD |

## Agents in This Workspace

**Primary wave agents**: `nw-product-discoverer`, `nw-product-owner`, `nw-solution-architect`, `nw-platform-architect`, `nw-acceptance-designer`, `nw-software-crafter`, `nw-functional-software-crafter`

**Cross-wave agents**: `nw-researcher`, `nw-troubleshooter`, `nw-documentarist`, `nw-data-engineer`, `nw-agent-builder`

**Reviewer agents** (invoked as subagents, not directly by users): `nw-software-crafter-reviewer`, `nw-acceptance-designer-reviewer`, `nw-solution-architect-reviewer`, `nw-platform-architect-reviewer`, `nw-product-owner-reviewer`, `nw-product-discoverer-reviewer`, `nw-documentarist-reviewer`, `nw-researcher-reviewer`, `nw-troubleshooter-reviewer`, `nw-data-engineer-reviewer`, `nw-agent-builder-reviewer`

## Slash Commands

Use these prompts to trigger wave execution (type `/` to see available prompts):

- `/nw-discover` — Start evidence-based product discovery
- `/nw-discuss` — JTBD analysis and requirements gathering
- `/nw-design` — Architecture design with C4 diagrams
- `/nw-devops` — CI/CD pipeline and infrastructure design
- `/nw-distill` — Create BDD acceptance tests
- `/nw-deliver` — Implement via Outside-In TDD
- `/nw-research` — Evidence-driven research with source verification
- `/nw-refactor` — Structured refactoring via RPP L1-L6 hierarchy
- `/nw-review` — Expert peer review of any artifact
- `/nw-new` — Start a new feature (guided wizard)
- `/nw-continue` — Resume a feature in progress
- `/nw-bugfix` — Bug fix workflow with root cause analysis

## Skill Library

Domain knowledge is stored in `nWave/skills/<name>/SKILL.md`. Agents load these files using the read tool at the appropriate phase. Do not move these files.

## Conventions

- **Feature artifacts**: `docs/feature/{feature-id}/{wave}/`
- **Execution log**: `docs/feature/{feature-id}/deliver/execution-log.json`
- **Roadmap**: `docs/feature/{feature-id}/deliver/roadmap.json`
- **Architecture**: `docs/architecture/architecture.md`, `docs/adrs/`
- **Research**: `docs/research/`
- **Commits**: conventional commits required — `feat|fix|docs|test|chore(scope): subject`
- **Code style**: Python ≥ 3.10, type hints, Ruff v0.15.0, line length 88, double quotes
- **Testing**: 5-layer framework — unit, integration, acceptance, e2e, mutation
- **Architecture**: hexagonal (ports & adapters), dependency inversion

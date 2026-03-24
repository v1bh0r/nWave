---
description: "[EXPERIMENTAL] Complex refactoring roadmaps using the Mikado Method. Use when architectural changes span multiple classes and simple refactoring is insufficient."
---

# NW-MIKADO: Complex Refactoring with Mikado Method

> **EXPERIMENTAL**: Under active development. Behavior and output format may change.

**Wave**: CROSS_WAVE

Invoke `#agent:nw-software-crafter` to plan and execute the Mikado refactoring.

## Usage

```
/nw-mikado [refactoring-goal] [--complexity=simple|moderate|complex] [--visualization=tree|graph]
```

## What is the Mikado Method?

A technique for complex refactoring that:
1. Tries a change, discovers what breaks
2. Commits the discovery (reverts the change, commits the dependency map)
3. Works bottom-up — fix leaves before the root
4. Builds a dependency tree of what must change first

## Agent Invocation

Invoke `#agent:nw-software-crafter`:

```
Execute Mikado Method refactoring for: {refactoring-goal}

Context:
- src/* — codebase to refactor
- docs/architecture/architecture-design.md — target architecture (if exists)

Configuration:
- complexity: {complexity}
- visualization: {tree|graph}
  - tree = indented markdown checklist
  - graph = Mermaid dependency diagram

Steps:
1. Attempt the goal change. Document what breaks.
2. Revert. Commit the dependency discovery: docs/mikado/{goal-name}.mikado.md
3. Repeat for each dependency until leaf nodes are reached.
4. Execute leaf-to-root: implement leaves first, then work up.
5. Each node complete = commit with: refactor({scope}): mikado {description}
```

## Success Criteria

- Mikado visualization at `docs/mikado/{goal-name}.mikado.md`
- All leaf nodes implemented before their parents
- All tests pass at each commit point
- Refactoring goal achieved without breaking changes

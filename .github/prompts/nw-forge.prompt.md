---
description: "Creates new specialized agents using the 5-phase workflow (ANALYZE > DESIGN > CREATE > VALIDATE > REFINE). Use when building a new AI agent or validating an existing agent specification."
---

# NW-FORGE: Create Agent

**Wave**: CROSS_WAVE

Invoke `#agent:nw-agent-builder` to create the new agent.

## Usage

```
/nw-forge [agent-name] [--type=specialist|reviewer|orchestrator] [--pattern=react|reflection|router]
```

## Agent Invocation

Invoke `#agent:nw-agent-builder`:

```
Create a new {type} agent named {agent-name}.

Configuration:
- agent_type: {type}  (specialist | reviewer | orchestrator)
- design_pattern: {pattern}  (react | reflection | router | planning | sequential | parallel | hierarchical)
- output_path: .github/agents/{agent-name}.agent.md

Requirements (V2 standards):
1. Agent definition 200-400 lines (under 400 strict)
2. Copilot frontmatter (description + tools only — no model field with Claude-specific values)
3. 14-point validation checklist passes
4. Only divergent behaviors specified (no Copilot defaults repeated)
5. 3-5 canonical examples included
6. Domain knowledge extracted to nWave/skills/{agent-name}/ if >50 lines
7. Skill paths use nWave/skills/<name>/SKILL.md (NOT ~/.claude/skills/)
8. Tools list uses Copilot aliases: read, edit, execute, search, agent, web
9. No TASK BOUNDARY or subagent guard language (Copilot-native)
10. Progressive write mandate for long-running agents
```

## Success Criteria

- Agent definition created at `.github/agents/{agent-name}.agent.md`
- File is under 400 lines
- No lint errors in YAML frontmatter
- Skill files created in `nWave/skills/{agent-name}/` if domain knowledge was extracted
- All 14 validation points pass

## After Creation

Run `#agent:nw-agent-builder-reviewer` to validate the new agent:
```
Review .github/agents/{agent-name}.agent.md against all 9 critique dimensions
and Copilot compatibility requirements.
```

---
description: "Guided wizard to start a new feature. Asks what you want to build, recommends the right starting wave, and launches it."
---

# NW-NEW: Start a New Feature

**Wave**: CROSS_WAVE (entry point)

This is a conversational wizard. Run directly — no agent invocation needed.

## Usage

```
/nw-new [feature-description]
```

## Wizard Flow

### Step 1: Feature Description Intake

If description is provided as argument, use it. If vague or missing, ask:
- What **system** is being changed?
- What **problem** are you solving?
- Who **benefits** from this change?

Example: "Add rate limiting to prevent API abuse"

### Step 2: Feature ID Derivation

Derive feature ID in kebab-case from the description:
- "Add rate limiting to the API gateway" → `rate-limiting-api-gateway`
- "OAuth2 upgrade" → `oauth2-upgrade`

Show derived ID and allow override.

### Step 3: Name Conflict Check

Check if `docs/feature/{feature-id}/` exists. If so, offer:
1. **Continue that project** — use `/nw-continue`
2. **Start fresh with different name** — ask for distinguishing name

### Step 4: Clarifying Questions

Ask:

**Q1: New or existing behavior?**
- New functionality that doesn't exist yet
- Changing/improving existing functionality
- Fixing a bug or regression

**Q2: Requirements readiness?**
- Clear requirements in my head
- Rough idea, need to explore
- Haven't validated the problem yet

**Q3: Codebase state?**
- Greenfield (no `src/` yet)
- Brownfield (existing codebase)

### Step 5: Wave Recommendation

| Scenario | Recommended start |
|----------|-------------------|
| Problem not yet validated | `/nw-discover` |
| Problem known, requirements unclear | `/nw-discuss` |
| Requirements clear, no architecture yet | `/nw-design` |
| Architecture done, ready to code | `/nw-distill` then `/nw-deliver` |
| Bug fix | `/nw-bugfix` |

Create `docs/feature/{feature-id}/` and launch the recommended wave.

"""Platform contract schemas -- single source of truth for cross-platform rules.

Defines canonical path rewrite mappings, forbidden fields, and exceptions
used by all OpenCode installer plugins. Every plugin that handles platform
differences MUST import from this module rather than hardcoding rules
locally (ADR-003).
"""

from __future__ import annotations


# -- Path Rewrite Rules (Claude Code -> OpenCode) ----------------------------
#
# Each entry maps a Claude Code path prefix to its OpenCode equivalent.
# Rules are applied in order; first match wins.
# More specific prefixes MUST appear before more general ones.

OPENCODE_PATH_REWRITES: tuple[tuple[str, str], ...] = (
    ("~/.claude/skills/", "~/.config/opencode/skills/"),
    ("~/.claude/agents/", "~/.config/opencode/agents/"),
    ("~/.claude/nWave/skills/", "~/.config/opencode/skills/"),
    ("~/.claude/nWave/", "~/.config/opencode/"),
)


# -- Path Rewrite Exceptions -------------------------------------------------
#
# Paths matching any of these prefixes are NEVER rewritten, even if they
# match a rewrite rule. The DES library path is the canonical example:
# it lives under ~/.claude/lib/python and must remain there.

OPENCODE_PATH_REWRITE_EXCEPTIONS: tuple[str, ...] = ("~/.claude/lib/python",)


# -- Skill Forbidden Fields (Claude Code only) -------------------------------
#
# YAML frontmatter fields that exist only in Claude Code's skill format.
# OpenCode does not recognize these fields; including them causes warnings
# or undefined behavior. The skills plugin MUST strip these during install.

OPENCODE_SKILL_FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "user-invocable",
        "disable-model-invocation",
    }
)


# -- Command Forbidden Fields (Claude Code only) ------------------------------
#
# YAML frontmatter fields that exist only in Claude Code's command format.
# OpenCode does not recognize these fields; the commands plugin MUST strip
# them during install.

OPENCODE_COMMAND_FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "argument-hint",
        "disable-model-invocation",
    }
)

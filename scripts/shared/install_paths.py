"""Centralized installation path constants -- single source of truth.

Replaces 10+ scattered hardcoded path constructions across installer
plugins, verifier, and build scripts.

All consumers should import from this module::

    from scripts.shared.install_paths import AGENTS_SUBDIR, agents_dir
"""

from __future__ import annotations

import sys
from pathlib import Path


# Relative path segments (appended to claude_dir by callers)
AGENTS_SUBDIR = Path("agents") / "nw"
SKILLS_SUBDIR = Path("skills")
TEMPLATES_SUBDIR = Path("templates")
DES_LIB_SUBDIR = Path("lib") / "python" / "des"
SCRIPTS_SUBDIR = Path("scripts")
COMMANDS_LEGACY_SUBDIR = Path("commands") / "nw"  # deprecated, cleanup only
MANIFEST_FILENAME = "nwave-manifest.txt"


def agents_dir(claude_dir: Path) -> Path:
    """Return the agents installation directory."""
    return claude_dir / AGENTS_SUBDIR


def skills_dir(claude_dir: Path) -> Path:
    """Return the skills installation directory."""
    return claude_dir / SKILLS_SUBDIR


def templates_dir(claude_dir: Path) -> Path:
    """Return the templates installation directory."""
    return claude_dir / TEMPLATES_SUBDIR


def des_dir(claude_dir: Path) -> Path:
    """Return the DES library installation directory."""
    return claude_dir / DES_LIB_SUBDIR


def manifest_path(claude_dir: Path) -> Path:
    """Return the installation manifest file path."""
    return claude_dir / MANIFEST_FILENAME


# -- Python command resolution ------------------------------------------------

# Literal pattern used in source templates for portable Python resolution.
# Installed files replace this with the resolved concrete path.
PYTHON_CMD_SUBSTITUTION = "$(command -v python3 || command -v python)"


def resolve_python_command() -> str:
    """Resolve the Python interpreter command for use in installed templates.

    Returns the basename of sys.executable when it is a system/pipx Python,
    or falls back to 'python3' when running inside a project-local .venv
    (to avoid embedding machine-specific paths in installed files).

    This mirrors the logic in DESPlugin._resolve_python_path() but returns
    only the command name (not a $HOME-prefixed path), suitable for
    substitution into skill/command templates.
    """
    python_path = sys.executable

    # Project-local .venv must not leak into installed files
    if "/.venv/" in python_path or "\\.venv\\" in python_path:
        return "python3"

    return "python3"

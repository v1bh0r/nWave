"""Shared utilities for attribution config read/write and hook lifecycle.

Used by AttributionPlugin (install-time) and CLI (post-install toggle).
The hook script does NOT import this module -- it reads JSON directly.
"""

import json
import os
import re
import shutil
import stat
import subprocess
import sys
from pathlib import Path


_SHELL_UNSAFE = re.compile(r"[;&|`(){}]")


_DEFAULT_TRAILER = "Co-Authored-By: nWave <nwave@nwave.ai>"
_HOOK_SCRIPT_NAME = "nwave_attribution_hook.py"
_HOOK_SHIM_NAME = "prepare-commit-msg"
_HOOK_ORIGINAL_SUFFIX = ".nwave-original"


def read_global_config(config_dir: Path) -> dict:
    """Read global-config.json, returning empty dict on error."""
    config_file = config_dir / "global-config.json"
    try:
        with open(config_file, encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def write_global_config(config_dir: Path, config: dict) -> None:
    """Write global-config.json with read-modify-write to preserve other keys."""
    config_dir.mkdir(parents=True, exist_ok=True)
    config_file = config_dir / "global-config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def read_attribution_preference(config_dir: Path) -> bool | None:
    """Read attribution preference from global config.

    Returns:
        True if enabled, False if disabled, None if not yet asked.
    """
    config = read_global_config(config_dir)
    attribution = config.get("attribution")
    if attribution is None:
        return None
    return attribution.get("enabled", False)


def write_attribution_preference(
    config_dir: Path,
    enabled: bool,
    trailer: str = _DEFAULT_TRAILER,
) -> None:
    """Write attribution preference, preserving other config keys."""
    config = read_global_config(config_dir)
    config["attribution"] = {
        "enabled": enabled,
        "trailer": trailer,
    }
    write_global_config(config_dir, config)


def _resolve_python_path() -> str:
    """Resolve Python interpreter path for hook shim.

    Same pattern as DESPlugin._resolve_python_path():
    captures sys.executable, replaces $HOME for portability,
    falls back to 'python3' for project-local .venv paths.
    """
    python_path = sys.executable

    if "/.venv/" in python_path or "\\.venv\\" in python_path:
        return "python3"

    home = str(Path.home())
    if python_path.startswith(home):
        python_path = "$HOME" + python_path[len(home) :]
    return python_path


def _resolve_hooks_dir() -> Path:
    """Resolve git global hooks directory.

    Checks core.hooksPath first. If not set, uses ~/.nwave/hooks/.
    """
    try:
        result = subprocess.run(
            ["git", "config", "--global", "core.hooksPath"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0 and result.stdout.strip():
            hooks_path = result.stdout.strip()
            # Expand ~ and $HOME
            hooks_path = os.path.expandvars(str(Path(hooks_path).expanduser()))
            return Path(hooks_path)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    return Path.home() / ".nwave" / "hooks"


def _set_hooks_path(hooks_dir: Path) -> None:
    """Set git global core.hooksPath if not already set."""
    try:
        result = subprocess.run(
            ["git", "config", "--global", "core.hooksPath"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0 or not result.stdout.strip():
            subprocess.run(
                ["git", "config", "--global", "core.hooksPath", str(hooks_dir)],
                capture_output=True,
                timeout=5,
            )
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass


def _read_shim_template() -> str:
    """Read the prepare-commit-msg shell shim template."""
    # Template is in nWave/templates/ relative to project root
    # At install time, it is copied to the installed location
    template_locations = [
        Path(__file__).parent.parent.parent
        / "nWave"
        / "templates"
        / "prepare-commit-msg.template",
        Path.home() / ".claude" / "templates" / "prepare-commit-msg.template",
    ]
    for loc in template_locations:
        if loc.exists():
            return loc.read_text(encoding="utf-8")

    # Fallback: inline template
    return (
        "#!/bin/sh\n"
        "# nWave attribution hook -- chains with existing hook\n"
        'HOOK_DIR="$(dirname "$0")"\n'
        'if [ -f "$HOOK_DIR/prepare-commit-msg.nwave-original" ]; then\n'
        '    "$HOOK_DIR/prepare-commit-msg.nwave-original" "$@" || exit $?\n'
        "fi\n"
        'if ! command -v "{{PYTHON_CMD}}" >/dev/null 2>&1; then\n'
        '    echo "nWave attribution: python3 not found, skipping" >&2\n'
        "    exit 0\n"
        "fi\n"
        '"{{PYTHON_CMD}}" "{{HOOK_SCRIPT_PATH}}" "$@"\n'
    )


def install_attribution_hook(config_dir: Path | None = None) -> Path:
    """Install prepare-commit-msg hook for attribution trailer.

    1. Resolve hooks directory from git config
    2. Copy hook script to ~/.nwave/hooks/
    3. If existing prepare-commit-msg, rename to .nwave-original
    4. Render and write shell shim as prepare-commit-msg
    5. Make executable

    Args:
        config_dir: Override for ~/.nwave/ (testing).

    Returns:
        Path to installed hook shim.
    """
    if config_dir is None:
        config_dir = Path.home() / ".nwave"

    hooks_dir = _resolve_hooks_dir()
    hooks_dir.mkdir(parents=True, exist_ok=True)

    # Copy hook script to config_dir/hooks/
    hook_dest_dir = config_dir / "hooks"
    hook_dest_dir.mkdir(parents=True, exist_ok=True)

    hook_source = Path(__file__).parent.parent / "hooks" / _HOOK_SCRIPT_NAME
    hook_dest = hook_dest_dir / _HOOK_SCRIPT_NAME
    if hook_source.exists():
        shutil.copy2(hook_source, hook_dest)

    # Handle existing prepare-commit-msg hook (chaining)
    shim_path = hooks_dir / _HOOK_SHIM_NAME
    original_path = hooks_dir / f"{_HOOK_SHIM_NAME}{_HOOK_ORIGINAL_SUFFIX}"

    if shim_path.exists():
        content = shim_path.read_text(encoding="utf-8")
        if "nwave_attribution_hook" in content:
            # Our shim already -- overwrite with updated version
            pass
        elif not original_path.exists():
            # Rename existing user hook to .nwave-original
            shim_path.rename(original_path)

    # Resolve paths for shim template, with shell-safety validation
    python_cmd = _resolve_python_path()
    if _SHELL_UNSAFE.search(python_cmd):
        python_cmd = "python3"  # fallback to safe default
    hook_script_path = str(hook_dest)
    if _SHELL_UNSAFE.search(hook_script_path):
        hook_script_path = str(config_dir / "hooks" / _HOOK_SCRIPT_NAME)
    home = str(Path.home())
    if hook_script_path.startswith(home):
        hook_script_path = "$HOME" + hook_script_path[len(home) :]

    # Render and write shim
    template = _read_shim_template()
    shim_content = template.replace("{{PYTHON_CMD}}", python_cmd)
    shim_content = shim_content.replace("{{HOOK_SCRIPT_PATH}}", hook_script_path)

    shim_path.write_text(shim_content, encoding="utf-8")
    shim_path.chmod(
        shim_path.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH
    )

    # Set core.hooksPath if needed
    _set_hooks_path(hooks_dir)

    # Record hooks_dir in config for deterministic uninstall
    config = read_global_config(config_dir)
    config.setdefault("attribution", {})["hooks_dir"] = str(hooks_dir)
    write_global_config(config_dir, config)

    return shim_path


def remove_attribution_hook(config_dir: Path | None = None) -> None:
    """Remove attribution hook and restore original if chained.

    Args:
        config_dir: Override for ~/.nwave/ (testing).
    """
    if config_dir is None:
        config_dir = Path.home() / ".nwave"

    # Read hooks_dir from config (deterministic uninstall)
    config = read_global_config(config_dir)
    hooks_dir_str = config.get("attribution", {}).get("hooks_dir")

    hooks_dir = Path(hooks_dir_str) if hooks_dir_str else _resolve_hooks_dir()

    shim_path = hooks_dir / _HOOK_SHIM_NAME
    original_path = hooks_dir / f"{_HOOK_SHIM_NAME}{_HOOK_ORIGINAL_SUFFIX}"

    # Only remove if it is our shim
    if shim_path.exists():
        try:
            content = shim_path.read_text(encoding="utf-8")
            if "nwave_attribution_hook" in content:
                shim_path.unlink()
        except OSError:
            pass

    # Restore original hook if it exists
    if original_path.exists():
        try:
            original_path.rename(shim_path)
        except OSError:
            pass

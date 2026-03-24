"""nwave-ai CLI: thin wrapper around nWave install/uninstall scripts."""

import subprocess
import sys
from pathlib import Path

from scripts.install.attribution_utils import (
    install_attribution_hook,
    read_attribution_preference,
    remove_attribution_hook,
    write_attribution_preference,
)


def _get_version() -> str:
    """Get version from package metadata (installed) or __init__.py (dev)."""
    from importlib.metadata import PackageNotFoundError, version

    try:
        return version("nwave-ai")
    except PackageNotFoundError:
        pass

    from nwave_ai import __version__

    return __version__


def _get_project_root() -> Path:
    """Find the project root (where scripts/install/ lives)."""
    return Path(__file__).parent.parent


def _run_script(script_name: str, args: list[str]) -> int:
    """Run an install script as a subprocess."""
    project_root = _get_project_root()
    script_path = project_root / "scripts" / "install" / script_name

    if not script_path.exists():
        print(f"Error: {script_name} not found at {script_path}", file=sys.stderr)
        print("The nwave-ai package may not be installed correctly.", file=sys.stderr)
        return 1

    cmd = [sys.executable, str(script_path), *args]
    result = subprocess.run(cmd, cwd=str(project_root))
    return result.returncode


def _is_workspace_scope(args: list[str]) -> bool:
    """Return True when args resolve to workspace scope (default)."""
    scope = "workspace"
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--scope" and i + 1 < len(args):
            scope = args[i + 1].strip().lower()
            i += 2
            continue
        if arg.startswith("--scope="):
            scope = arg.split("=", 1)[1].strip().lower()
        i += 1
    return scope == "workspace"


def _has_explicit_target(args: list[str]) -> bool:
    """Return True when --target is already provided."""
    for arg in args:
        if arg == "--target" or arg.startswith("--target="):
            return True
    return False


def _with_default_workspace_target(args: list[str]) -> list[str]:
    """Inject --target=<cwd> for workspace scope when target is omitted.

    This preserves expected behavior when running 'nwave-ai copilot-*' from any
    project directory even though scripts execute from the package root.
    """
    if _has_explicit_target(args):
        return args
    if not _is_workspace_scope(args):
        return args
    return [*args, f"--target={Path.cwd()}"]


def _get_config_dir() -> Path:
    """Return the nWave config directory (~/.nwave/)."""
    return Path.home() / ".nwave"


def _handle_attribution(args: list[str]) -> int:
    """Handle 'attribution on|off|status' subcommand."""
    if not args:
        print("Usage: nwave-ai attribution <on|off|status>", file=sys.stderr)
        return 1

    action = args[0].lower()
    config_dir = _get_config_dir()

    if action == "on":
        write_attribution_preference(config_dir, enabled=True)
        install_attribution_hook(config_dir)
        print("Attribution enabled. Your commits will include the nWave credit line.")
        return 0

    if action == "off":
        write_attribution_preference(config_dir, enabled=False)
        remove_attribution_hook(config_dir)
        print(
            "Attribution disabled. Your commits will not include the nWave credit line."
        )
        return 0

    if action == "status":
        preference = read_attribution_preference(config_dir)
        if preference is True:
            print("Attribution is currently on.")
        else:
            print("Attribution is currently off.")
        return 0

    print(f"Unknown attribution action: {action}", file=sys.stderr)
    print("Usage: nwave-ai attribution <on|off|status>", file=sys.stderr)
    return 1


def _print_usage() -> int:
    ver = _get_version()
    print(f"nwave-ai {ver}")
    print()
    print("Usage: nwave-ai <command> [options]")
    print()
    print("Commands:")
    print("  install              Install nWave framework to ~/.claude/")
    print("  uninstall            Remove nWave framework from ~/.claude/")
    print("  copilot-install      Install nWave Copilot agents/prompts (workspace or global)")
    print("  copilot-uninstall    Remove nWave Copilot agents/prompts")
    print("  copilot-status       Show Copilot agents installation status")
    print("  attribution          Toggle commit attribution (on/off/status)")
    print("  version              Show nwave-ai version")
    print()
    print("Install options:")
    print("  --dry-run            Preview without making changes")
    print("  --backup-only        Create backup only")
    print("  --restore            Restore from backup")
    print()
    print("Copilot install options:")
    print("  --scope=workspace    Install into current workspace .github/ (default)")
    print("  --scope=global       Install into ~/.github/ for all VS Code workspaces")
    print("  --target=PATH        Explicit workspace root (workspace scope only)")
    print("  --from-github=REPO   Download latest agents from GitHub; accepts")
    print("                       'owner/repo', 'owner/repo@branch', or full URL")
    print("  --dry-run            Preview without writing files")
    print("  --verbose, -v        Print each file as it is installed")
    print("  --force              Reinstall even if already installed")
    print()
    print("Examples:")
    print("  nwave-ai install")
    print("  nwave-ai copilot-install")
    print("  nwave-ai copilot-install --from-github=v1bh0r/nWave")
    print("  nwave-ai copilot-install --scope=global")
    print("  nwave-ai copilot-install --target=/path/to/my-project")
    print("  nwave-ai copilot-uninstall --scope=global")
    return 0


def main() -> int:
    """CLI entry point for nwave-ai."""
    if len(sys.argv) < 2 or sys.argv[1] in ("--help", "-h", "help"):
        return _print_usage()

    command = sys.argv[1]

    if command == "install":
        return _run_script("install_nwave.py", sys.argv[2:])
    elif command == "uninstall":
        return _run_script("uninstall_nwave.py", sys.argv[2:])
    elif command == "copilot-install":
        copilot_args = _with_default_workspace_target(sys.argv[2:])
        return _run_script("install_copilot_agents.py", ["install", *copilot_args])
    elif command == "copilot-uninstall":
        copilot_args = _with_default_workspace_target(sys.argv[2:])
        return _run_script("install_copilot_agents.py", ["uninstall", *copilot_args])
    elif command == "copilot-status":
        copilot_args = _with_default_workspace_target(sys.argv[2:])
        return _run_script("install_copilot_agents.py", ["status", *copilot_args])
    elif command == "attribution":
        return _handle_attribution(sys.argv[2:])
    elif command == "version":
        print(f"nwave-ai {_get_version()}")
        return 0
    else:
        print(f"Unknown command: {command}", file=sys.stderr)
        print("Run 'nwave-ai --help' for usage.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

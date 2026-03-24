#!/usr/bin/env python3
"""
nWave Copilot Agents Installer

Installs nWave GitHub Copilot agent (.agent.md) and prompt (.prompt.md) files
for use with GitHub Copilot in VS Code.

Scopes:
  workspace  Copy to {target}/.github/  (default: current working directory)
  global     Copy to ~/.github/         (VS Code user-level Copilot customization)

Usage:
  nwave-ai copilot-install [--scope=workspace|global] [--target=PATH] [--dry-run] [--verbose]
  python install_copilot_agents.py install [--scope=workspace|global] [options]
  python install_copilot_agents.py uninstall [--scope=workspace|global] [options]
"""

import argparse
import json
import shutil
import sys
import tarfile
import tempfile
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


_MANIFEST_FILENAME = ".nwave-copilot-manifest.json"
_AGENTS_SUBDIR = "agents"
_PROMPTS_SUBDIR = "prompts"
_COPILOT_INSTRUCTIONS = "copilot-instructions.md"


# ---------------------------------------------------------------------------
# Source discovery
# ---------------------------------------------------------------------------


def _get_project_root() -> Path:
    """Return the nWave project root (two levels up from this script)."""
    return Path(__file__).parent.parent.parent


def _find_source_github_dir() -> Path | None:
    """Locate the .github/ source directory containing agent and prompt files.

    Checks the project root for a .github/agents/ directory.
    Returns None if not found.
    """
    project_root = _get_project_root()
    candidate = project_root / ".github"
    if candidate.exists() and (candidate / _AGENTS_SUBDIR).exists():
        return candidate
    return None


# ---------------------------------------------------------------------------
# GitHub download
# ---------------------------------------------------------------------------


def _parse_github_repo(value: str) -> tuple[str, str]:
    """Parse a GitHub repo identifier into (owner/repo, branch).

    Accepts:
      - "owner/repo"
      - "owner/repo@branch"
      - "https://github.com/owner/repo"
      - "https://github.com/owner/repo/tree/branch"

    Returns (owner/repo, branch).
    """
    branch = "main"

    # Strip scheme
    for prefix in ("https://github.com/", "http://github.com/", "github.com/"):
        if value.startswith(prefix):
            value = value[len(prefix):].rstrip("/")
            break

    # Handle tree/branch suffix: owner/repo/tree/branch
    parts = value.split("/")
    if len(parts) >= 4 and parts[2] == "tree":
        repo = f"{parts[0]}/{parts[1]}"
        branch = "/".join(parts[3:])
        return repo, branch

    # Handle @branch suffix: owner/repo@branch
    if "@" in value:
        repo, branch = value.split("@", 1)
        return repo.strip("/"), branch

    return value.strip("/"), branch


def _download_from_github(
    repo_spec: str,
    verbose: bool = False,
) -> Path | None:
    """Download nWave .github/ files from a public GitHub repository.

    Downloads the tarball for the specified branch, extracts it to a temporary
    directory, and returns the path to the .github/ directory within it.
    The caller is responsible for deleting the temp directory after use.

    Args:
        repo_spec: "owner/repo", "owner/repo@branch", or full GitHub URL.
        verbose: print download progress.

    Returns:
        Path to the extracted .github/ directory, or None on failure.
    """
    repo, branch = _parse_github_repo(repo_spec)

    if repo.count("/") != 1:
        print(
            f"Error: Invalid repository '{repo}'. Expected format: owner/repo",
            file=sys.stderr,
        )
        return None

    url = f"https://github.com/{repo}/archive/refs/heads/{branch}.tar.gz"
    if verbose:
        print(f"  Downloading {repo}@{branch} ...")
        print(f"  URL: {url}")
    else:
        print(f"  Downloading {repo}@{branch} from GitHub ...")

    tmp_dir = Path(tempfile.mkdtemp(prefix="nwave-copilot-"))
    tarball = tmp_dir / "archive.tar.gz"

    try:
        urllib.request.urlretrieve(url, tarball)  # noqa: S310 (http is fine for public repos)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            print(
                f"Error: Repository or branch not found: {repo}@{branch}",
                file=sys.stderr,
            )
        else:
            print(f"Error: GitHub returned HTTP {exc.code} for {url}", file=sys.stderr)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None
    except urllib.error.URLError as exc:
        print(f"Error: Network error — {exc.reason}", file=sys.stderr)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"Error: {exc}", file=sys.stderr)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None

    extract_dir = tmp_dir / "extract"
    extract_dir.mkdir()
    try:
        with tarfile.open(tarball, "r:gz") as tar:
            try:
                tar.extractall(extract_dir, filter="data")  # Python 3.12+ safe extraction
            except TypeError:
                tar.extractall(extract_dir)  # Python < 3.12
    except tarfile.TarError as exc:
        print(f"Error: Failed to extract archive — {exc}", file=sys.stderr)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None

    # The tarball extracts to a single root dir named "{repo_name}-{branch}"
    extracted_roots = [d for d in extract_dir.iterdir() if d.is_dir()]
    if not extracted_roots:
        print("Error: Archive appears to be empty.", file=sys.stderr)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None

    github_dir = extracted_roots[0] / ".github"
    if not github_dir.exists() or not (github_dir / "agents").exists():
        print(
            f"Error: No .github/agents/ directory found in {repo}@{branch}.\n"
            "Make sure this is an nWave repository.",
            file=sys.stderr,
        )
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return None

    if verbose:
        print(f"  Extracted to {tmp_dir}")

    return github_dir


# ---------------------------------------------------------------------------
# Target paths
# ---------------------------------------------------------------------------


def _global_github_dir() -> Path:
    """Return the VS Code user-level .github directory (~/.github/)."""
    return Path.home() / ".github"


def _resolve_target_github(scope: str, target: Path | None) -> Path:
    """Resolve the target .github/ directory based on scope and optional override."""
    if scope == "global":
        return _global_github_dir()
    base = target if target is not None else Path.cwd()
    return base / ".github"


# ---------------------------------------------------------------------------
# Manifest helpers
# ---------------------------------------------------------------------------


def _read_manifest(github_dir: Path) -> dict:
    """Read the installation manifest from the target directory."""
    manifest_path = github_dir / _MANIFEST_FILENAME
    if manifest_path.exists():
        try:
            return json.loads(manifest_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {"installed_files": [], "installed_at": None, "scope": None, "version": None}


def _write_manifest(github_dir: Path, manifest: dict, dry_run: bool) -> None:
    """Write the installation manifest to track installed files."""
    if dry_run:
        return
    manifest_path = github_dir / _MANIFEST_FILENAME
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# File operations
# ---------------------------------------------------------------------------


def _copy_directory(
    source_dir: Path,
    target_dir: Path,
    pattern: str,
    label: str,
    dry_run: bool,
    verbose: bool,
) -> list[str]:
    """Copy files matching a glob pattern from source_dir into target_dir.

    Returns a list of destination file paths that were (or would be) installed.
    """
    if not source_dir.exists():
        return []

    source_files = sorted(source_dir.glob(pattern))
    if not source_files:
        return []

    count = len(source_files)
    print(f"  {label} ({count} files) → .github/{target_dir.name}/")

    if not dry_run:
        target_dir.mkdir(parents=True, exist_ok=True)

    installed: list[str] = []
    for src in source_files:
        dst = target_dir / src.name
        if verbose or dry_run:
            prefix = "    [dry-run] " if dry_run else "    "
            print(f"{prefix}→ {dst.name}")
        if not dry_run:
            shutil.copy2(src, dst)
        installed.append(str(dst))

    return installed


# ---------------------------------------------------------------------------
# Version helper
# ---------------------------------------------------------------------------


def _get_nwave_version() -> str:
    """Return the installed nwave-ai version or 'unknown'."""
    try:
        from importlib.metadata import PackageNotFoundError, version

        return version("nwave-ai")
    except Exception:
        return "unknown"


# ---------------------------------------------------------------------------
# Next-steps guidance
# ---------------------------------------------------------------------------


def _print_next_steps(scope: str, target_github: Path, agent_count: int, prompt_count: int) -> None:
    """Print post-installation guidance."""
    print()
    if scope == "workspace":
        print("  To use in VS Code:")
        print("    1. Open this directory as a VS Code workspace")
        print("    2. Open GitHub Copilot Chat (Ctrl+Alt+I / Cmd+Option+I)")
        print("    3. Type  #agent:nw-  to see available nWave agents")
        print("    4. Use   /  in the prompt input to browse nWave slash commands")
    else:
        print("  To use in VS Code (global — available in all workspaces):")
        print("    1. Open GitHub Copilot Chat in any project")
        print("    2. Type  #agent:nw-  to see available nWave agents")
        print("    3. Use   /  in the prompt input to browse nWave slash commands")
    print()
    print(f"  Agents installed   : {agent_count}")
    print(f"  Prompts installed  : {prompt_count}")
    print(f"  Location           : {target_github}")


# ---------------------------------------------------------------------------
# Install command
# ---------------------------------------------------------------------------


def install(
    scope: str,
    target: Path | None,
    dry_run: bool,
    verbose: bool,
    force: bool,
    source_override: Path | None = None,
) -> int:
    """Install nWave GitHub Copilot agents and prompts.

    Args:
        scope: "workspace" or "global"
        target: explicit target directory path (workspace scope only)
        dry_run: preview without writing files
        verbose: show each file as it is copied
        force: reinstall even if already installed
        source_override: use this .github/ directory instead of auto-detecting.

    Returns:
        Exit code (0 = success, 1 = error)
    """
    if source_override is not None:
        source_github = source_override
    else:
        source_github = _find_source_github_dir()
    if source_github is None:
        print(
            "Error: Cannot locate nWave .github/ source directory.",
            file=sys.stderr,
        )
        print(
            "Run this command from the nWave project root, or install via 'nwave-ai'.",
            file=sys.stderr,
        )
        return 1

    target_github = _resolve_target_github(scope, target)
    scope_label = (
        f"global  (~/.github/)" if scope == "global" else f"workspace  ({target_github.parent})"
    )

    # Guard: already installed
    manifest = _read_manifest(target_github)
    if manifest.get("installed_files") and not force:
        prev_version = manifest.get("version", "unknown")
        prev_date = manifest.get("installed_at", "unknown")
        print(f"nWave Copilot agents already installed (version {prev_version}, {prev_date}).")
        print(f"  Location: {target_github}")
        print()
        print("Use --force to reinstall, or 'nwave-ai copilot-uninstall' to remove.")
        return 0

    print(f"Installing nWave Copilot agents [{scope_label}]")
    if dry_run:
        print("  (dry-run — no files will be written)")
    print()

    installed_files: list[str] = []

    # --- Agents ---
    agents = _copy_directory(
        source_dir=source_github / _AGENTS_SUBDIR,
        target_dir=target_github / _AGENTS_SUBDIR,
        pattern="*.agent.md",
        label="Agents",
        dry_run=dry_run,
        verbose=verbose,
    )
    installed_files.extend(agents)

    # --- Prompts ---
    prompts = _copy_directory(
        source_dir=source_github / _PROMPTS_SUBDIR,
        target_dir=target_github / _PROMPTS_SUBDIR,
        pattern="*.prompt.md",
        label="Prompts",
        dry_run=dry_run,
        verbose=verbose,
    )
    installed_files.extend(prompts)

    # --- copilot-instructions.md (workspace scope only — it's workspace-specific context) ---
    if scope == "workspace":
        src_instructions = source_github / _COPILOT_INSTRUCTIONS
        if src_instructions.exists():
            dst_instructions = target_github / _COPILOT_INSTRUCTIONS
            print(f"  Instructions (1 file) → .github/copilot-instructions.md")
            if verbose or dry_run:
                prefix = "    [dry-run] " if dry_run else "    "
                print(f"{prefix}→ copilot-instructions.md")
            if not dry_run:
                target_github.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_instructions, dst_instructions)
            installed_files.append(str(dst_instructions))

    # Write manifest
    new_manifest = {
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "scope": scope,
        "version": _get_nwave_version(),
        "installed_files": installed_files,
    }
    _write_manifest(target_github, new_manifest, dry_run)

    print()
    if dry_run:
        print(f"  [dry-run] Would install {len(installed_files)} files to {target_github}")
    else:
        print(f"  ✅  Installed {len(installed_files)} files")
        _print_next_steps(scope, target_github, len(agents), len(prompts))

    return 0


# ---------------------------------------------------------------------------
# Uninstall command
# ---------------------------------------------------------------------------


def uninstall(
    scope: str,
    target: Path | None,
    dry_run: bool,
    verbose: bool,
) -> int:
    """Remove nWave GitHub Copilot files using the installation manifest.

    Args:
        scope: "workspace" or "global"
        target: explicit target directory path (workspace scope only)
        dry_run: preview without removing files
        verbose: show each file as it is removed

    Returns:
        Exit code (0 = success, 1 = error)
    """
    target_github = _resolve_target_github(scope, target)
    manifest = _read_manifest(target_github)
    installed_files = manifest.get("installed_files", [])

    if not installed_files:
        print(f"No nWave Copilot installation found at {target_github}.")
        print("Nothing to uninstall.")
        return 0

    count = len(installed_files)
    scope_label = "global" if scope == "global" else f"workspace ({target_github.parent})"
    print(f"Uninstalling nWave Copilot agents [{scope_label}]")
    if dry_run:
        print("  (dry-run — no files will be removed)")
    print()

    removed = 0
    for file_path in installed_files:
        path = Path(file_path)
        if path.exists():
            if verbose or dry_run:
                prefix = "  [dry-run] " if dry_run else "  "
                print(f"{prefix}✗ {path.name}")
            if not dry_run:
                path.unlink()
                removed += 1

    # Remove manifest itself
    manifest_path = target_github / _MANIFEST_FILENAME
    if not dry_run and manifest_path.exists():
        manifest_path.unlink()

    print()
    if dry_run:
        print(f"  [dry-run] Would remove {count} files from {target_github}")
    else:
        print(f"  ✅  Removed {removed} files from {target_github}")

    return 0


# ---------------------------------------------------------------------------
# Status command
# ---------------------------------------------------------------------------


def status(scope: str, target: Path | None) -> int:
    """Show current installation status.

    Args:
        scope: "workspace" or "global"
        target: explicit target directory path (workspace scope only)

    Returns:
        Exit code (0 = installed, 1 = not installed)
    """
    target_github = _resolve_target_github(scope, target)
    manifest = _read_manifest(target_github)
    installed_files = manifest.get("installed_files", [])

    if not installed_files:
        print(f"Not installed  ({target_github})")
        return 1

    version = manifest.get("version", "unknown")
    installed_at = manifest.get("installed_at", "unknown")
    agent_count = sum(1 for f in installed_files if f.endswith(".agent.md"))
    prompt_count = sum(1 for f in installed_files if f.endswith(".prompt.md"))

    print(f"Installed  ({target_github})")
    print(f"  Version    : {version}")
    print(f"  Date       : {installed_at}")
    print(f"  Agents     : {agent_count}")
    print(f"  Prompts    : {prompt_count}")
    print(f"  Total files: {len(installed_files)}")
    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


def main() -> int:
    """Parse arguments and dispatch to install/uninstall/status."""
    parser = argparse.ArgumentParser(
        prog="install_copilot_agents",
        description="Install nWave GitHub Copilot agents and prompts into a workspace or globally.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Install into the current workspace (default, from bundled files)
  python install_copilot_agents.py

  # Install the LATEST agents straight from GitHub
    nwave-ai copilot-install --from-github=v1bh0r/nWave

  # Install globally for all VS Code workspaces
  python install_copilot_agents.py --scope=global

  # Install into a specific project directory
  python install_copilot_agents.py --target=/path/to/my-project

  # Preview what would be installed without writing any files
  python install_copilot_agents.py --dry-run --verbose

  # Uninstall from current workspace
  python install_copilot_agents.py uninstall

  # Show installation status
  python install_copilot_agents.py status
""",
    )

    parser.add_argument(
        "action",
        nargs="?",
        default="install",
        choices=["install", "uninstall", "status"],
        help="Action to perform (default: install)",
    )
    parser.add_argument(
        "--scope",
        choices=["workspace", "global"],
        default="workspace",
        help=(
            "Installation scope: "
            "'workspace' copies to {target}/.github/ (default: cwd); "
            "'global' copies to ~/.github/ for use across all VS Code workspaces"
        ),
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=None,
        metavar="PATH",
        help="Root of the target workspace directory (workspace scope only; default: cwd)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview which files would be installed without writing anything",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print each file as it is installed or removed",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Reinstall even if nWave Copilot agents are already installed",
    )
    parser.add_argument(
        "--from-github",
        metavar="REPO",
        default=None,
        help=(
            "Download the latest agents directly from a GitHub repository instead of using "
            "the bundled files. Accepts 'owner/repo', 'owner/repo@branch', or a full GitHub "
            "URL (e.g. --from-github=v1bh0r/nWave). Requires internet access."
        ),
    )

    args = parser.parse_args()

    if args.action == "install":
        source_override: Path | None = None
        _tmp_dir: Path | None = None
        if args.from_github:
            github_dir = _download_from_github(args.from_github, verbose=args.verbose)
            if github_dir is None:
                return 1
            source_override = github_dir
            _tmp_dir = github_dir.parent.parent  # tmp root created by _download_from_github
        try:
            return install(
                scope=args.scope,
                target=args.target,
                dry_run=args.dry_run,
                verbose=args.verbose,
                force=args.force,
                source_override=source_override,
            )
        finally:
            if _tmp_dir is not None:
                shutil.rmtree(_tmp_dir, ignore_errors=True)
    elif args.action == "uninstall":
        return uninstall(
            scope=args.scope,
            target=args.target,
            dry_run=args.dry_run,
            verbose=args.verbose,
        )
    else:
        return status(
            scope=args.scope,
            target=args.target,
        )


if __name__ == "__main__":
    sys.exit(main())

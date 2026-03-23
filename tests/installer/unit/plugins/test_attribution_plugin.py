"""Unit tests for AttributionPlugin.

Tests validate install-time consent flow through the driving port
(AttributionPlugin.install/verify) and assert at driven port boundaries
(global-config.json file system).

Test Budget: 6 behaviors x 2 = 12 max. Using 6 tests (1 per behavior).

Behaviors tested:
1. Interactive accept default -> attribution enabled in config
2. Interactive decline -> attribution disabled in config
3. Non-interactive (no TTY) -> defaults off, no prompt issued
4. Existing preference -> prompt skipped (upgrade path)
5. Missing config directory -> created automatically
6. Plugin error -> never blocks core installation (exception-safe)
"""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

from scripts.install.plugins.attribution_plugin import AttributionPlugin
from scripts.install.plugins.base import InstallContext


def _make_context(tmp_path: Path) -> InstallContext:
    """Create a minimal InstallContext with tmp_path-based directories."""
    claude_dir = tmp_path / ".claude"
    claude_dir.mkdir(parents=True)

    return InstallContext(
        claude_dir=claude_dir,
        scripts_dir=tmp_path / "scripts",
        templates_dir=tmp_path / "templates",
        logger=MagicMock(),
        project_root=tmp_path / "project",
        metadata={"nwave_config_dir": tmp_path / ".nwave"},
    )


def _read_global_config(config_dir: Path) -> dict:
    """Read global-config.json from the given nwave config directory."""
    config_file = config_dir / "global-config.json"
    with open(config_file, encoding="utf-8") as f:
        return json.load(f)


class TestAttributionPluginInstall:
    """Tests for AttributionPlugin.install() driving port."""

    def test_interactive_accept_default(self, tmp_path: Path) -> None:
        """TTY present, empty input (default) -> attribution enabled."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        plugin = AttributionPlugin(config_dir=nwave_dir)

        with (
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input", return_value=""),
        ):
            mock_stdin.isatty.return_value = True
            result = plugin.install(context)

        assert result.success is True
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is True
        assert (
            config["attribution"]["trailer"] == "Co-Authored-By: nWave <nwave@nwave.ai>"
        )

    def test_interactive_decline(self, tmp_path: Path) -> None:
        """TTY present, input 'n' -> attribution disabled."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        plugin = AttributionPlugin(config_dir=nwave_dir)

        with (
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input", return_value="n"),
        ):
            mock_stdin.isatty.return_value = True
            result = plugin.install(context)

        assert result.success is True
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is False

    def test_non_interactive_defaults_off(self, tmp_path: Path) -> None:
        """No TTY -> attribution defaults to off, no prompt issued."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        plugin = AttributionPlugin(config_dir=nwave_dir)

        with (
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input") as mock_input,
        ):
            mock_stdin.isatty.return_value = False
            result = plugin.install(context)

        assert result.success is True
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is False
        mock_input.assert_not_called()

    def test_existing_preference_skips_prompt(self, tmp_path: Path) -> None:
        """Config already has attribution key -> no prompt, preserve preference."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        nwave_dir.mkdir(parents=True)
        config_file = nwave_dir / "global-config.json"
        existing_config = {
            "attribution": {
                "enabled": True,
                "trailer": "Co-Authored-By: nWave <nwave@nwave.ai>",
            }
        }
        config_file.write_text(json.dumps(existing_config), encoding="utf-8")

        plugin = AttributionPlugin(config_dir=nwave_dir)

        with patch("builtins.input") as mock_input:
            result = plugin.install(context)

        assert result.success is True
        mock_input.assert_not_called()
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is True

    def test_missing_config_dir_created(self, tmp_path: Path) -> None:
        """Config directory does not exist -> created, preference stored."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave-fresh"
        assert not nwave_dir.exists()

        plugin = AttributionPlugin(config_dir=nwave_dir)

        with (
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input", return_value="y"),
        ):
            mock_stdin.isatty.return_value = True
            result = plugin.install(context)

        assert result.success is True
        assert nwave_dir.exists()
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is True

    def test_never_blocks_core_install(self, tmp_path: Path) -> None:
        """Plugin error returns success with warning, never blocks install."""
        context = _make_context(tmp_path)
        # Use a path that will cause write failure (file instead of directory)
        nwave_dir = tmp_path / ".nwave-bad"
        nwave_dir.mkdir(parents=True)
        # Create a file where global-config.json should be a file in a dir
        # that cannot be created (simulate write error)
        config_file = nwave_dir / "global-config.json"
        # Make the config file a directory to cause json.dump to fail
        config_file.mkdir(parents=True)

        plugin = AttributionPlugin(config_dir=nwave_dir)

        with (
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input", return_value="y"),
        ):
            mock_stdin.isatty.return_value = True
            result = plugin.install(context)

        # Must succeed even on error -- never block core install
        assert result.success is True
        assert result.plugin_name == "attribution"


class TestAttributionPluginVerify:
    """Tests for AttributionPlugin.verify() driving port."""

    def test_verify_passes_with_attribution_key(self, tmp_path: Path) -> None:
        """Verify passes when config has attribution key."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        nwave_dir.mkdir(parents=True)
        config_file = nwave_dir / "global-config.json"
        config_file.write_text(
            json.dumps({"attribution": {"enabled": True}}),
            encoding="utf-8",
        )

        plugin = AttributionPlugin(config_dir=nwave_dir)
        result = plugin.verify(context)

        assert result.success is True

    def test_verify_passes_without_config_file(self, tmp_path: Path) -> None:
        """Verify passes even without config file (attribution is optional)."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave-missing"
        plugin = AttributionPlugin(config_dir=nwave_dir)
        result = plugin.verify(context)

        # Attribution is optional -- missing config is valid
        assert result.success is True


class TestAttributionPluginMetadata:
    """Tests for plugin registration metadata."""

    def test_plugin_priority_is_200(self) -> None:
        """Plugin priority must be 200 (runs after all core plugins)."""
        plugin = AttributionPlugin()
        assert plugin.priority == 200

    def test_plugin_name_is_attribution(self) -> None:
        """Plugin name must be 'attribution'."""
        plugin = AttributionPlugin()
        assert plugin.name == "attribution"


class TestAttributionUpgradePreservation:
    """Tests for US-04: upgrade preserves attribution preference."""

    def test_upgrade_preserves_enabled(self, tmp_path: Path) -> None:
        """Existing enabled preference -> no prompt, preference preserved."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        nwave_dir.mkdir(parents=True)
        config_file = nwave_dir / "global-config.json"
        config_file.write_text(
            json.dumps(
                {
                    "attribution": {
                        "enabled": True,
                        "trailer": "Co-Authored-By: nWave <nwave@nwave.ai>",
                    }
                }
            ),
            encoding="utf-8",
        )

        plugin = AttributionPlugin(config_dir=nwave_dir)

        with patch("builtins.input") as mock_input:
            result = plugin.install(context)

        assert result.success is True
        mock_input.assert_not_called()
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is True
        assert (
            "preserved" in result.message.lower() or "enabled" in result.message.lower()
        )

    def test_upgrade_preserves_disabled(self, tmp_path: Path) -> None:
        """Existing disabled preference -> no prompt, preference preserved."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        nwave_dir.mkdir(parents=True)
        config_file = nwave_dir / "global-config.json"
        config_file.write_text(
            json.dumps(
                {
                    "attribution": {
                        "enabled": False,
                        "trailer": "Co-Authored-By: nWave <nwave@nwave.ai>",
                    }
                }
            ),
            encoding="utf-8",
        )

        plugin = AttributionPlugin(config_dir=nwave_dir)

        with patch("builtins.input") as mock_input:
            result = plugin.install(context)

        assert result.success is True
        mock_input.assert_not_called()
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is False

    def test_upgrade_missing_preference_prompts(self, tmp_path: Path) -> None:
        """Config exists but no attribution key -> prompts like fresh install."""
        context = _make_context(tmp_path)
        nwave_dir = tmp_path / ".nwave"
        nwave_dir.mkdir(parents=True)
        config_file = nwave_dir / "global-config.json"
        # Config exists but no attribution key
        config_file.write_text(
            json.dumps({"rigor": {"level": "standard"}}),
            encoding="utf-8",
        )

        plugin = AttributionPlugin(config_dir=nwave_dir)

        with (
            patch("sys.stdin") as mock_stdin,
            patch("builtins.input", return_value="y"),
        ):
            mock_stdin.isatty.return_value = True
            result = plugin.install(context)

        assert result.success is True
        config = _read_global_config(nwave_dir)
        assert config["attribution"]["enabled"] is True
        # Rigor key preserved
        assert config["rigor"]["level"] == "standard"

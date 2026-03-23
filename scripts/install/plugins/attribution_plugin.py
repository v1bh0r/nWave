"""Attribution plugin for install-time consent prompt.

Prompts the developer to opt in to Co-Authored-By trailer in commits.
Runs LAST (priority 200) -- never blocks core installation.
"""

import sys
from pathlib import Path

from scripts.install.attribution_utils import (
    install_attribution_hook,
    read_attribution_preference,
    remove_attribution_hook,
    write_attribution_preference,
)

from .base import InstallationPlugin, InstallContext, PluginResult


_PROMPT = (
    "Would you like to credit nWave in your commits? (Co-Authored-By trailer) [Y/n] "
)
_MSG_ENABLED = "Attribution enabled. Change anytime: nwave-ai attribution off"
_MSG_DISABLED = "No problem. nWave works exactly the same either way."


class AttributionPlugin(InstallationPlugin):
    """Install-time attribution consent prompt.

    Priority 200: runs after all core plugins (agents=10, commands=20,
    skills=30, des=50, templates=60, utilities=70).
    """

    def __init__(self, config_dir: Path | None = None):
        super().__init__(name="attribution", priority=200)
        self._config_dir = config_dir or Path.home() / ".nwave"

    def install(self, context: InstallContext) -> PluginResult:
        """Prompt for attribution consent and store preference.

        Never raises -- all errors caught and returned as success
        with a warning message (attribution must not block install).
        """
        try:
            return self._do_install(context)
        except Exception as e:
            context.logger.warning(
                f"  Attribution setup encountered an error: {e}. "
                "Enable manually: nwave-ai attribution on"
            )
            return PluginResult(
                success=True,
                plugin_name="attribution",
                message=f"Attribution skipped due to error: {e}",
            )

    def _do_install(self, context: InstallContext) -> PluginResult:
        """Core install logic, may raise."""
        existing = read_attribution_preference(self._config_dir)

        if existing is not None:
            state = "enabled" if existing else "disabled"
            context.logger.info(
                f"  Attribution already {state}, keeping existing preference."
            )
            # Ensure hook state matches preference (self-heal on upgrade)
            if existing:
                install_attribution_hook(self._config_dir)
            return PluginResult(
                success=True,
                plugin_name="attribution",
                message=f"Attribution preference preserved ({state})",
            )

        if not sys.stdin.isatty():
            write_attribution_preference(self._config_dir, enabled=False)
            context.logger.info(
                "  Non-interactive install: attribution defaults to off."
            )
            return PluginResult(
                success=True,
                plugin_name="attribution",
                message="Attribution disabled (non-interactive)",
            )

        response = input(_PROMPT).strip().lower()
        enabled = response in ("", "y", "yes")

        write_attribution_preference(self._config_dir, enabled=enabled)

        if enabled:
            install_attribution_hook(self._config_dir)
            context.logger.info(f"  {_MSG_ENABLED}")
        else:
            context.logger.info(f"  {_MSG_DISABLED}")

        return PluginResult(
            success=True,
            plugin_name="attribution",
            message=_MSG_ENABLED if enabled else _MSG_DISABLED,
        )

    def verify(self, context: InstallContext) -> PluginResult:
        """Verify attribution config exists (not whether hook exists).

        Attribution is optional -- missing config is valid (not yet asked).
        """
        try:
            preference = read_attribution_preference(self._config_dir)
            if preference is not None:
                state = "enabled" if preference else "disabled"
                return PluginResult(
                    success=True,
                    plugin_name="attribution",
                    message=f"Attribution is {state}",
                )
            return PluginResult(
                success=True,
                plugin_name="attribution",
                message="Attribution not yet configured (optional)",
            )
        except Exception as e:
            return PluginResult(
                success=True,
                plugin_name="attribution",
                message=f"Attribution verify skipped: {e}",
            )

    def uninstall(self, context: InstallContext) -> PluginResult:
        """Remove attribution hook and config key."""
        try:
            remove_attribution_hook(self._config_dir)

            from scripts.install.attribution_utils import (
                read_global_config,
                write_global_config,
            )

            config = read_global_config(self._config_dir)
            config.pop("attribution", None)
            write_global_config(self._config_dir, config)
            return PluginResult(
                success=True,
                plugin_name="attribution",
                message="Attribution preference and hook removed",
            )
        except Exception as e:
            return PluginResult(
                success=True,
                plugin_name="attribution",
                message=f"Attribution uninstall skipped: {e}",
            )

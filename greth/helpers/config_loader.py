"""Project entrypoint for Greth Offensive."""

from __future__ import annotations

from rich.prompt import Prompt, Confirm

from greth.core.blackboard import Blackboard
from greth.core.config import GrethConfig
from greth.core.scheduler import CampaignScheduler
from greth.helpers.config_loader import load_or_create_default_config
from greth.tui.app import ConsoleUI


def run() -> int:
    """Run Greth without CLI flags or environment exports.

    Settings are loaded from ~/.greth_offensive/config.yml. If missing or incomplete,
    the user is prompted via the built-in console UI.
    """
    config = load_or_create_default_config()
    ui = ConsoleUI()
    ui.render_header()

    if not config.target or config.target == "https://example.com":
        config.target = Prompt.ask("Target URL", default=config.target)
    if not config.mode:
        config.mode = Prompt.ask("Execution mode", choices=["recon", "offense", "full"], default="full")

    if not Confirm.ask("Proceed with campaign?", default=True):
        ui.render_cancelled()
        return 0

    scheduler = CampaignScheduler(config=config, blackboard=Blackboard(), ui=ui)
    scheduler.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

"""Project entrypoint for Greth Offensive."""

from __future__ import annotations

import argparse
from typing import Sequence

from greth.core.config import GrethConfig
from greth.core.graph import build_graph
from greth.core.scheduler import CampaignScheduler


def run(argv: Sequence[str] | None = None) -> int:
    """Run the Greth intelligence engine."""
    parser = argparse.ArgumentParser(description="Greth Offensive")
    parser.add_argument("--target", default="https://example.com", help="Target URL or scope")
    parser.add_argument("--mode", choices=["recon", "offense", "full"], default="full", help="Campaign mode")
    parser.add_argument("--model", default="gpt-4o-mini", help="LiteLLM-compatible model")
    args = parser.parse_args(list(argv) if argv is not None else None)

    config = GrethConfig(target=args.target, mode=args.mode, model=args.model)
    graph = build_graph(config)
    scheduler = CampaignScheduler(graph=graph, config=config)
    scheduler.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

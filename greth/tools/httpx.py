"""HTTPX-compatible tool stub."""

from __future__ import annotations

from greth.tools.base import BaseTool


class HTTPXTool(BaseTool):
    name = "httpx"

    def run(self, target: str, **kwargs):
        return {
            "target": target,
            "status": "ok",
            "summary": f"HTTPX probe queued for {target}",
        }

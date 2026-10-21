"""Registry for security tools."""

from __future__ import annotations

from greth.tools.internet import INTERNET, InternetTool
from greth.tools.terminal import TERMINAL, TerminalTool

TOOL_REGISTRY = {
    "internet": INTERNET,
    "terminal": TERMINAL,
    "httpx": INTERNET,
    "bash": TERMINAL,
}


def get_tool(name: str):
    tool = TOOL_REGISTRY.get(name)
    if tool is None:
        raise KeyError(f"Unknown tool: {name}")
    return tool

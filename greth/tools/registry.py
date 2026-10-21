"""Registry for security tools."""

from __future__ import annotations

from greth.tools.httpx import HTTPXTool

TOOL_REGISTRY = {
    "httpx": HTTPXTool,
}


def get_tool(name: str, **kwargs):
    return TOOL_REGISTRY[name](**kwargs)

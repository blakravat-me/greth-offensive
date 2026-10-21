"""Tool wrappers and adapters."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class ToolResult:
    name: str
    success: bool
    output: Any
    metadata: dict[str, Any] | None = None


class BaseTool:
    """Low-level execution primitive for use by agents."""

    name = "base"

    def run(self, *args: Any, **kwargs: Any) -> ToolResult:
        return ToolResult(name=self.name, success=True, output={}, metadata={})

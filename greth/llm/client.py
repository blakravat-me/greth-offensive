"""LiteLLM + LangGraph provider layer."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from litellm import completion


@dataclass(slots=True)
class LLMConfig:
    model: str = "gpt-4o-mini"
    api_key: str | None = None
    base_url: str | None = None
    provider: str = "openai"


class LiteLLMClient:
    """Thin wrapper for asynchronous and sync LiteLLM usage."""

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig()

    def invoke(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        response = completion(
            model=self.config.model,
            messages=messages,
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            **kwargs,
        )
        return response["choices"][0]["message"]["content"]

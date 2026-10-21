"""LLM prompt and schema helpers."""

from __future__ import annotations

from pydantic import BaseModel


class AgentPrompt(BaseModel):
    role: str
    content: str


class FindingSchema(BaseModel):
    target: str
    kind: str
    confidence: float
    summary: str

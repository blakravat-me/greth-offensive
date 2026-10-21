"""Security helper utilities."""

from __future__ import annotations

import re


def is_valid_target(value: str) -> bool:
    return bool(value) and (value.startswith("http://") or value.startswith("https://") or value.startswith("ws://"))


def normalize_target(value: str) -> str:
    return value.strip().rstrip("/")


def sanitize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()

"""HTTP and web-surface tooling for offensive reconnaissance."""

from __future__ import annotations

import re
from typing import Any

import httpx

from greth.tools.base import BaseTool


class InternetTool(BaseTool):
    """HTTP/HTTPS fetcher and endpoint extractor for the swarm."""

    name = "internet"

    def __init__(self, *, timeout: int = 15, user_agent: str = "greth-offensive/0.1") -> None:
        self.timeout = timeout
        self.user_agent = user_agent

    def fetch(self, target: str, *, method: str = "GET", headers: dict[str, str] | None = None) -> dict[str, Any]:
        request_headers = {"User-Agent": self.user_agent}
        if headers:
            request_headers.update(headers)

        response = httpx.request(method.upper(), target, headers=request_headers, timeout=self.timeout, follow_redirects=True)
        return {
            "target": target,
            "method": method.upper(),
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "ok": response.is_success,
            "text": response.text,
            "url": str(response.url),
            "final_url": str(response.url),
            "content_type": response.headers.get("content-type", ""),
        }

    def extract_endpoints(self, target: str, text: str) -> list[str]:
        candidates = re.findall(r"https?://[^\s\"'<>]+", text)
        ordered: list[str] = []
        seen: set[str] = set()
        for candidate in candidates:
            normalized = candidate.rstrip(".,;)")
            if normalized not in seen:
                seen.add(normalized)
                ordered.append(normalized)
        if not ordered:
            return [target]
        return ordered[:20]


INTERNET = InternetTool()

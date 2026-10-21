"""Internet access utilities using httpx."""

from __future__ import annotations

import re
from urllib.parse import urljoin

import httpx


class InternetTool:
    """Fetch and parse remote content in a lightweight way."""

    def fetch(self, url: str, timeout: int = 20) -> dict:
        response = httpx.get(url, timeout=timeout, follow_redirects=True)
        response.raise_for_status()
        return {
            "url": str(response.url),
            "status_code": response.status_code,
            "content_type": response.headers.get("content-type", ""),
            "text": response.text,
        }

    def extract_endpoints(self, url: str, html: str | None = None) -> list[str]:
        if html is None:
            html = self.fetch(url)["text"]
        references = re.findall(r'''(?:href|src)=["']([^"']+)['"]''', html, flags=re.IGNORECASE)
        endpoints = []
        for item in references:
            if item.startswith(("http://", "https://")):
                endpoints.append(item)
            elif item.startswith("/"):
                endpoints.append(urljoin(url, item))
        return endpoints


INTERNET = InternetTool()

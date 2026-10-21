"""Reconnaissance agent with internet and terminal probes."""

from __future__ import annotations

from greth.agents.base import AgentBase
from greth.tools.internet import INTERNET
from greth.tools.terminal import TERMINAL


class ReconnaissanceAgent(AgentBase):
    name = "reconnaissance"

    def trigger(self, finding) -> bool:
        return finding.kind in {"TARGET_REGISTERED"}

    def handle(self, finding):
        target = finding.target
        result = INTERNET.fetch(target)
        endpoints = INTERNET.extract_endpoints(target, result["text"])
        findings = []

        self.publish(
            kind="HTTP_ENDPOINT",
            target=target,
            payload={"endpoint": target, "status_code": result["status_code"]},
            confidence=0.9,
            summary=f"Target {target} responded successfully",
        )

        for endpoint in endpoints[:10]:
            findings.append(
                self.publish(
                    kind="HTTP_ENDPOINT",
                    target=endpoint,
                    payload={"source": target},
                    confidence=0.75,
                    summary=f"Discovered endpoint {endpoint}",
                )
            )

        probe = TERMINAL.run(f"curl -I --max-time 15 '{target}' 2>/dev/null | head")
        if probe["ok"]:
            findings.append(
                self.publish(
                    kind="TECHNOLOGY",
                    target=target,
                    payload={"tool": "curl", "stdout": probe["stdout"][:200]},
                    confidence=0.6,
                    summary=f"Curl verification for {target}",
                )
            )

        return findings

"""Report agent: writes a summary artifact for the campaign."""

from __future__ import annotations

from pathlib import Path

from greth.agents.base import AgentBase


class ReportAgent(AgentBase):
    name = "report"

    def trigger(self, finding) -> bool:
        return finding.kind in {"SESSION", "AGENT_ERROR", "VULNERABILITY", "EXPLOIT_CHAIN"}

    def handle(self, finding):
        output_dir = Path.home() / ".greth_offensive" / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        report_path = output_dir / "campaign_report.txt"
        report = (
            f"Greth Offensive Campaign Report\n"
            f"Target: {finding.target}\n"
            f"Finding kind: {finding.kind}\n"
            f"Confidence: {finding.confidence}\n"
            f"Summary: {finding.summary}\n"
        )
        with report_path.open("a", encoding="utf-8") as handle:
            handle.write(report + "\n---\n")
        return self.publish(
            kind="CAMPAIGN_COMPLETE",
            target=finding.target,
            payload={"report_path": str(report_path)},
            confidence=1.0,
            summary=f"Campaign report saved at {report_path}",
        )

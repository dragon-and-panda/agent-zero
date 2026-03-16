from __future__ import annotations


class MCPRouter:
    """Lightweight MCP integration shim.

    This MVP does not directly execute remote MCP calls; it returns suggested
    services based on context so an external orchestrator can route requests.
    """

    def __init__(self, enabled_services: list[str] | None = None) -> None:
        self._enabled = enabled_services or [
            "policy-lookup",
            "building-code-check",
            "image-evidence-analyzer",
            "document-verifier",
            "wallet-monitor",
        ]

    def list_services(self) -> list[str]:
        return list(self._enabled)

    def suggest_services(self, text: str) -> list[str]:
        lowered = text.lower()
        suggested: list[str] = []
        if any(k in lowered for k in ("code", "permit", "authority", "inspection")):
            suggested.append("building-code-check")
        if any(k in lowered for k in ("photo", "image", "video", "evidence")):
            suggested.append("image-evidence-analyzer")
        if any(k in lowered for k in ("document", "invoice", "certificate", "report")):
            suggested.append("document-verifier")
        if any(k in lowered for k in ("wallet", "escrow", "usdt", "tx")):
            suggested.append("wallet-monitor")
        if any(k in lowered for k in ("policy", "term", "arbitration", "compliance")):
            suggested.append("policy-lookup")
        # Keep ordering stable and constrained to enabled list.
        return [s for s in dict.fromkeys(suggested) if s in self._enabled]

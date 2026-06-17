import subprocess

from python.helpers import files
from python.helpers.tool import Response, Tool


class RevenuePlanning(Tool):
    async def execute(
        self,
        venture: str = "",
        assets: str = "",
        data_sources: str = "",
        consent_model: str = "",
        monetization: str = "",
        legality: str = "",
        consent: str = "",
        provenance: str = "",
        platform_risk: str = "",
        time_to_cash: str = "",
        margin: str = "",
        repeatability: str = "",
        automation_fit: str = "",
        defensibility: str = "",
        **kwargs,
    ):
        compliance_pack = files.read_file("docs/policies/compliance_pack.md")
        score_result = self._run_score(
            legality=legality,
            consent=consent,
            provenance=provenance,
            platform_risk=platform_risk,
            time_to_cash=time_to_cash,
            margin=margin,
            repeatability=repeatability,
            automation_fit=automation_fit,
            defensibility=defensibility,
        )

        unsafe_reason = self._detect_disallowed_pattern(
            venture=venture,
            data_sources=data_sources,
            consent_model=consent_model,
            monetization=monetization,
        )
        if unsafe_reason:
            redirect = self.agent.read_prompt(
                "tool.revenue_planning.reject.md",
                venture=venture or "unspecified venture",
                unsafe_reason=unsafe_reason,
                score_result=score_result or "not scored",
            )
            return Response(message=redirect, break_loop=False)

        system = self.agent.read_prompt("tool.revenue_planning.sys.md")
        message = self.agent.read_prompt(
            "tool.revenue_planning.msg.md",
            venture=venture or "unspecified",
            assets=assets or "not provided",
            data_sources=data_sources or "not provided",
            consent_model=consent_model or "not provided",
            monetization=monetization or "not provided",
            legality=legality or "not provided",
            consent=consent or "not provided",
            provenance=provenance or "not provided",
            platform_risk=platform_risk or "not provided",
            time_to_cash=time_to_cash or "not provided",
            margin=margin or "not provided",
            repeatability=repeatability or "not provided",
            automation_fit=automation_fit or "not provided",
            defensibility=defensibility or "not provided",
            score_result=score_result or "not scored",
            compliance_pack=compliance_pack,
        )
        plan = await self.agent.call_utility_model(
            system=system, message=message, background=False
        )
        return Response(message=plan.strip(), break_loop=False)

    def _run_score(
        self,
        *,
        legality: str,
        consent: str,
        provenance: str,
        platform_risk: str,
        time_to_cash: str,
        margin: str,
        repeatability: str,
        automation_fit: str,
        defensibility: str,
    ) -> str:
        factors = [
            legality,
            consent,
            provenance,
            platform_risk,
            time_to_cash,
            margin,
            repeatability,
            automation_fit,
            defensibility,
        ]
        if not all(self._is_score_value(value) for value in factors):
            return ""

        cmd = [
            files.get_abs_path("instruments/strategy/score.sh"),
            legality,
            consent,
            provenance,
            platform_risk,
            time_to_cash,
            margin,
            repeatability,
            automation_fit,
            defensibility,
        ]
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return completed.stdout.strip()

    def _is_score_value(self, value: str) -> bool:
        return value.strip().lower() in {"low", "medium", "high"}

    def _detect_disallowed_pattern(
        self,
        *,
        venture: str,
        data_sources: str,
        consent_model: str,
        monetization: str,
    ) -> str:
        combined = " ".join([venture, data_sources, consent_model, monetization]).lower()

        blocked_groups = [
            (
                ("sell", "email"),
                "personal email addresses or contact lists cannot be sold or brokered",
            ),
            (
                ("broker", "email"),
                "personal email addresses or contact lists cannot be sold or brokered",
            ),
            (
                ("gmail", "list"),
                "gmail or mailbox data cannot be turned into contact inventories for resale",
            ),
            (
                ("inbox", "sell"),
                "inbox contents cannot be monetized through contact resale",
            ),
            (
                ("scrape", "email"),
                "scraping email addresses for outreach or resale is prohibited",
            ),
            (
                ("harvest", "email"),
                "harvesting email addresses is prohibited",
            ),
            (
                ("cold outreach",),
                "non-consensual cold outreach based on acquired contacts is out of scope",
            ),
            (
                ("mailbox", "resale"),
                "mailbox-derived data cannot be repackaged for resale",
            ),
        ]

        for keywords, reason in blocked_groups:
            if all(keyword in combined for keyword in keywords):
                return reason
        return ""

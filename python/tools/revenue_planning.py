from python.helpers.tool import Response, Tool


class RevenuePlanning(Tool):
    async def execute(
        self,
        mission="",
        assets="",
        constraints="",
        target_market="",
        data_sources="",
        go_to_market="",
        **kwargs,
    ):
        lines = [
            "# Revenue planning brief",
            "",
            f"Mission: {mission or 'Not provided'}",
            f"Assets: {assets or 'Not provided'}",
            f"Constraints: {constraints or 'Not provided'}",
            f"Target market: {target_market or 'Not provided'}",
            f"Data sources: {data_sources or 'Not provided'}",
            f"Go-to-market ideas: {go_to_market or 'Not provided'}",
            "",
            "## Mandatory legality and ethics gates",
            "- Require explicit consent for personal-data use, inbox access, and outreach.",
            "- Reject spam, contact-list resale, credential abuse, scraping behind auth, and platform-rule evasion.",
            "- Prefer first-party assets, licensed datasets, opt-in audiences, and transparent value exchange.",
            "",
            "## Planning outputs to produce next",
            "1. Opportunity shortlist with legality, consent, and unit-economics notes.",
            "2. Data handling plan with provenance, retention, and deletion rules.",
            "3. MVP go-to-market plan using opt-in acquisition channels.",
            "4. Risks, blockers, and evidence gaps that require research.",
            "",
            "Use the compliance pack, incoming strategy queue, and score instrument before recommending execution.",
        ]
        return Response(message="\n".join(lines), break_loop=False)

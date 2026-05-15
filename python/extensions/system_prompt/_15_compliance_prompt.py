from python.helpers import files
from python.helpers.extension import Extension
from agent import LoopData


COMPLIANCE_PACK_PATH = "docs/policies/compliance_pack.md"


class CompliancePrompt(Extension):

    async def execute(self, system_prompt: list[str] = [], loop_data: LoopData = LoopData(), **kwargs):
        if files.exists(COMPLIANCE_PACK_PATH):
            rules = files.read_file(COMPLIANCE_PACK_PATH)
            system_prompt.insert(0, f"## Compliance pack\n{rules}")

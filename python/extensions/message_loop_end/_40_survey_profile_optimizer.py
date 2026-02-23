from agent import LoopData
from python.helpers.extension import Extension
from python.helpers.survey_runtime import DATA_NAME_SURVEY_RUNTIME


class SurveyProfileOptimizer(Extension):
    async def execute(self, loop_data: LoopData = LoopData(), **kwargs):
        runtime = self.agent.get_data(DATA_NAME_SURVEY_RUNTIME)
        if not runtime:
            return
        if runtime.is_busy():
            return
        runtime.maybe_start_background_optimizer(self.agent)

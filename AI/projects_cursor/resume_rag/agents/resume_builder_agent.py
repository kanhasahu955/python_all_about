from agents.base_agent import BaseAgent

class ResumeBuilderAgent(BaseAgent):

    async def execute(self, state):

        state["optimized_resume"] = """
        Generated Resume Here
        """

        return state
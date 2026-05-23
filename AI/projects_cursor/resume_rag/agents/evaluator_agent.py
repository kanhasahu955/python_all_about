from agents.base_agent import BaseAgent

class EvaluatorAgent(BaseAgent):

    async def execute(self, state):

        state["final_score"] = 92

        return state
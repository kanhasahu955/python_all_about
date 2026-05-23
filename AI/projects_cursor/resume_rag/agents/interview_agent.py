from agents.base_agent import BaseAgent

class InterviewAgent(BaseAgent):

    async def execute(self, state):

        skills = state["skills"]

        state["questions"] = [
            "Explain FastAPI Architecture",
            "Explain LangGraph",
            "Explain Snowflake"
        ]

        return state
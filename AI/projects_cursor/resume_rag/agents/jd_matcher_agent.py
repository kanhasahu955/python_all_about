from agents.base_agent import BaseAgent

class JDMatcherAgent(BaseAgent):
    async def execute(self, state):
        jd = state["job_description"]
        resume = state["resume_text"]
        prompt = f"""
        Compare JD and Resume.

        Give:

        Score
        Missing Skills
        Improvements
        """

        state["jd_match"] = prompt

        return state
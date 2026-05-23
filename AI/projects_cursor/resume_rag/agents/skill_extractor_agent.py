from agents.base_agent import BaseAgent
from langchain_openai import ChatOpenAI

class SkillExtractorAgent(BaseAgent):
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4.1"
        )

    async def execute(self, state):
        prompt = f"""
        Extract:
        Skills
        Experience
        Education

        Resume:
        {state['resume_text']}
        """
        response = self.llm.invoke(prompt)
        state["skills"] = response.content

        return state
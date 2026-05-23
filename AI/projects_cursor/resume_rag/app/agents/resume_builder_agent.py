from app.agents.base_agent import BaseAgent
from app.core.config import settings


class ResumeBuilderAgent(BaseAgent):
    def execute(self, state):
        resume = state.get("resume_text", "")
        jd = state.get("job_description", "")

        if settings.OPENAI_API_KEY:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
            prompt = f"""
Optimize this resume for the target job. Return markdown.

Job Description:
{jd}

Resume:
{resume}
"""
            response = llm.invoke(prompt)
            state["optimized_resume"] = response.content
        else:
            state["optimized_resume"] = f"# Optimized Resume\n\n{resume}"

        return state

from app.agents.base_agent import BaseAgent
from app.core.config import settings


class JDMatcherAgent(BaseAgent):
    def execute(self, state):
        jd = state.get("job_description", "")
        resume = state.get("resume_text", "")

        if settings.OPENAI_API_KEY and jd:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
            prompt = f"""
Compare the job description and resume.
Return JSON with keys: score (0-100), missing_skills (list), improvements (list).

Job Description:
{jd}

Resume:
{resume}
"""
            response = llm.invoke(prompt)
            state["jd_match_json"] = response.content
        else:
            state["jd_match_json"] = (
                '{"score": 0, "missing_skills": [], '
                '"improvements": ["Add OPENAI_API_KEY and job description for matching"]}'
            )

        return state

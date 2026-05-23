import json

from app.agents.base_agent import BaseAgent
from app.core.config import settings


class SkillExtractorAgent(BaseAgent):
    def execute(self, state):
        resume_text = state.get("resume_text", "")

        if settings.OPENAI_API_KEY:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.OPENAI_API_KEY)
            prompt = f"""
Extract skills, experience, and education from this resume.
Return JSON with keys: skills (list), experience (list), education (list).

Resume:
{resume_text}
"""
            response = llm.invoke(prompt)
            state["skills_json"] = response.content
        else:
            # Fallback when no API key: basic keyword extraction
            words = [w.strip(".,()") for w in resume_text.split() if len(w) > 3]
            state["skills_json"] = json.dumps({"skills": list(set(words))[:20]})

        return state

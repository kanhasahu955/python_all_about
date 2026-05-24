import json

from app.agents.base_agent import BaseAgent
from app.core.llm import get_chat_llm, llm_configured


class InterviewAgent(BaseAgent):
    def execute(self, state):
        skills = state.get("skills", "")
        resume_text = state.get("resume_text", "")

        if llm_configured():
            llm = get_chat_llm()
            prompt = f"""
Generate 8 technical interview questions based on the skills and background below.
Return JSON with key "questions" as a list of strings.

Skills:
{skills}

Resume context:
{resume_text[:4000]}
"""
            response = llm.invoke(prompt)
            content = response.content.strip()
            try:
                parsed = json.loads(content)
                questions = parsed.get("questions", [content])
            except json.JSONDecodeError:
                questions = [line.strip("- ").strip() for line in content.splitlines() if line.strip()]
            state["interview_questions"] = json.dumps({"questions": questions})
        else:
            state["interview_questions"] = json.dumps(
                {"questions": [f"Explain your experience with {skill.strip()}" for skill in skills.split(",")[:5] if skill.strip()]}
            )

        return state

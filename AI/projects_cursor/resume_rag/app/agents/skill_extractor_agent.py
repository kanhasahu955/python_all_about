import json

from app.agents.base_agent import BaseAgent
from app.core.llm import llm_configured
from app.core.llm_stream import stream_chat_response


class SkillExtractorAgent(BaseAgent):
    agent_name = "extract_skills"

    def execute(self, state):
        self._start(state)
        resume_text = state.get("resume_text", "")
        document_id = state.get("document_id")

        if llm_configured():
            prompt = f"""
Extract skills, experience, and education from this resume.
Return JSON with keys: skills (list), experience (list), education (list).

Resume:
{resume_text}
"""
            state["skills_json"] = stream_chat_response(document_id, "extract_skills", prompt)
        else:
            words = [w.strip(".,()") for w in resume_text.split() if len(w) > 3]
            state["skills_json"] = json.dumps({"skills": list(set(words))[:20]})

        return state

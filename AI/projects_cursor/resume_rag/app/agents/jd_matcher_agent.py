from app.agents.base_agent import BaseAgent
from app.core.llm import llm_configured
from app.core.llm_stream import stream_chat_response


class JDMatcherAgent(BaseAgent):
    agent_name = "match_jd"

    def execute(self, state):
        self._start(state)
        jd = state.get("job_description", "")
        resume = state.get("resume_text", "")
        document_id = state.get("document_id")

        if llm_configured() and jd:
            prompt = f"""
Compare the job description and resume.
Return JSON with keys: score (0-100), missing_skills (list), improvements (list).

Job Description:
{jd}

Resume:
{resume}
"""
            state["jd_match_json"] = stream_chat_response(document_id, "match_jd", prompt)
        else:
            state["jd_match_json"] = (
                '{"score": 0, "missing_skills": [], '
                '"improvements": ["Add GROQ_API_KEY and job description for matching"]}'
            )

        return state

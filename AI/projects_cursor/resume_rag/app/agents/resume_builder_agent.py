from app.agents.base_agent import BaseAgent
from app.core.llm import llm_configured
from app.core.llm_stream import stream_chat_response
from app.services.resume_build_service import build_resume_prompt


class ResumeBuilderAgent(BaseAgent):
    agent_name = "build_resume"

    def execute(self, state):
        self._start(state)
        resume = state.get("resume_text", "")
        jd = state.get("job_description", "")
        jd_match = state.get("jd_match_json", "")
        document_id = state.get("document_id")

        if llm_configured():
            prompt = build_resume_prompt(
                resume_text=resume,
                job_description=jd,
                jd_match_json=jd_match,
            )
            state["optimized_resume"] = stream_chat_response(
                document_id,
                "build_resume",
                prompt,
            )
        else:
            state["optimized_resume"] = f"# Optimized Resume\n\n{resume}"

        return state

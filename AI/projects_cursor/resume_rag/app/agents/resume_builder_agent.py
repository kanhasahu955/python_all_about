from app.agents.base_agent import BaseAgent
from app.core.llm import llm_configured
from app.core.llm_stream import stream_chat_response


class ResumeBuilderAgent(BaseAgent):
    agent_name = "build_resume"

    def execute(self, state):
        self._start(state)
        resume = state.get("resume_text", "")
        jd = state.get("job_description", "")
        document_id = state.get("document_id")

        if llm_configured():
            prompt = f"""
Optimize this resume for the target job. Return markdown.

Job Description:
{jd}

Resume:
{resume}
"""
            state["optimized_resume"] = stream_chat_response(
                document_id,
                "build_resume",
                prompt,
            )
        else:
            state["optimized_resume"] = f"# Optimized Resume\n\n{resume}"

        return state

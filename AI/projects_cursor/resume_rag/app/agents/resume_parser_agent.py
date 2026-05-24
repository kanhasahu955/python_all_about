from pypdf import PdfReader

from app.agents.base_agent import BaseAgent
from app.services.agent_events import agent_events


class ResumeParserAgent(BaseAgent):
    agent_name = "parse_resume"

    def execute(self, state):
        self._start(state)
        file_path = state["file_path"]
        document_id = state.get("document_id")
        reader = PdfReader(file_path)
        total = len(reader.pages)
        text = ""

        for index, page in enumerate(reader.pages):
            text += page.extract_text() or ""
            if document_id:
                agent_events.publish_agent_progress(
                    document_id,
                    "parse_resume",
                    f"Reading page {index + 1} of {total}…",
                    partial=text[-400:] if text else None,
                )

        state["resume_text"] = text.strip()
        return state

from pypdf import PdfReader

from app.agents.base_agent import BaseAgent


class ResumeParserAgent(BaseAgent):
    def execute(self, state):
        file_path = state["file_path"]
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        state["resume_text"] = text.strip()
        return state

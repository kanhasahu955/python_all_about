from pypdf import PdfReader
from agents.base_agent import BaseAgent

class ResumeParserAgent(BaseAgent):
    async def execute(self, state):
        file_path = state["resume_path"]
        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        state["resume_text"] = text
        return state
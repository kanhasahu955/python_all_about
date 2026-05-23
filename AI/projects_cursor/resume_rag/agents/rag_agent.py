from agents.base_agent import BaseAgent
from rag.retriever import ResumeRetriever

class RAGAgent(BaseAgent):

    async def execute(self, state):

        retriever = ResumeRetriever()

        docs = retriever.search(
            state["job_description"]
        )

        state["context"] = docs

        return state
from app.agents.base_agent import BaseAgent
from app.rag.retriever import ResumeRetriever


class RAGAgent(BaseAgent):
    def execute(self, state):
        query = state.get("job_description") or state.get("resume_text", "")

        try:
            retriever = ResumeRetriever()
            matches = retriever.search(query, top_k=5)
            state["rag_context"] = "\n\n".join(
                m.get("metadata", {}).get("text", "") for m in matches
            )
        except Exception as exc:
            state["rag_context"] = f"RAG unavailable: {exc}"

        return state

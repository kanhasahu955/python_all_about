from app.agents.base_agent import BaseAgent
from app.core.llm import llm_configured
from app.core.llm_stream import stream_chat_response
from app.rag.retriever import ResumeRetriever
from app.services.agent_events import agent_events


class RAGAgent(BaseAgent):
    agent_name = "rag_search"

    def execute(self, state):
        self._start(state)
        query = state.get("job_description") or state.get("resume_text", "")
        document_id = state.get("document_id")

        if document_id:
            agent_events.publish_agent_progress(
                document_id,
                "rag_search",
                "Querying Pinecone vector store…",
            )

        try:
            retriever = ResumeRetriever()
            matches = retriever.search(query, top_k=5)
            context = "\n\n".join(
                m.get("metadata", {}).get("text", "") for m in matches
            )
            state["rag_context"] = context

            if document_id:
                preview = context[:400] + ("…" if len(context) > 400 else "")
                agent_events.publish_agent_progress(
                    document_id,
                    "rag_search",
                    f"Retrieved {len(matches)} similar chunk(s)",
                    partial=preview or "No matches yet",
                )
        except Exception as exc:
            state["rag_context"] = f"RAG unavailable: {exc}"
            if document_id:
                agent_events.publish_agent_progress(
                    document_id,
                    "rag_search",
                    f"RAG unavailable: {exc}",
                )

        return state

from typing import TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from pydantic import BaseModel, Field

from app.config import settings
from app.rag.pinecone_store import query_similar


class AnalysisResult(BaseModel):
    fit_score: int = Field(ge=0, le=100, description="0-100 alignment with the job")
    strengths: list[str] = Field(default_factory=list)
    gaps: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    summary: str = ""


class AgentState(TypedDict):
    namespace: str
    job_description: str
    context_chunks: list[str]
    analysis: AnalysisResult | None


async def retrieve_node(state: AgentState) -> AgentState:
    matches = await query_similar(
        namespace=state["namespace"],
        query=state["job_description"],
        top_k=10,
    )
    chunks = [m["text"] for m in matches if m.get("text")]
    return {**state, "context_chunks": chunks}


async def analyze_node(state: AgentState) -> AgentState:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=settings.openai_api_key or None,
        temperature=0.2,
    )
    structured = llm.with_structured_output(AnalysisResult)
    context = "\n---\n".join(state["context_chunks"]) or "(no retrieved chunks)"
    messages = [
        SystemMessage(
            content=(
                "You are an expert recruiter. Compare the candidate resume excerpts "
                "to the job description. Be specific and grounded in the excerpts."
            )
        ),
        HumanMessage(
            content=(
                f"Job description:\n{state['job_description']}\n\n"
                f"Resume excerpts:\n{context}\n\n"
                "Produce the structured analysis."
            )
        ),
    ]
    result: AnalysisResult = await structured.ainvoke(messages)
    return {**state, "analysis": result}


def build_graph():
    g = StateGraph(AgentState)
    g.add_node("retrieve", retrieve_node)
    g.add_node("analyze", analyze_node)
    g.set_entry_point("retrieve")
    g.add_edge("retrieve", "analyze")
    g.add_edge("analyze", END)
    return g.compile()


graph_app = build_graph()

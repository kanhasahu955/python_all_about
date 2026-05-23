from typing import TypedDict, NotRequired
from langgraph.graph import StateGraph, END

from app.agents.resume_parser_agent import ResumeParserAgent
from app.agents.skill_extractor_agent import SkillExtractorAgent
from app.agents.rag_agent import RAGAgent
from app.agents.jd_matcher_agent import JDMatcherAgent
from app.agents.resume_builder_agent import ResumeBuilderAgent


class ResumeGraphState(TypedDict):
    document_id: str
    file_path: str
    job_description: NotRequired[str]
    resume_text: NotRequired[str]
    skills_json: NotRequired[str]
    rag_context: NotRequired[str]
    jd_match_json: NotRequired[str]
    optimized_resume: NotRequired[str]


def build_resume_graph():
    graph = StateGraph(ResumeGraphState)

    graph.add_node("parse_resume", ResumeParserAgent().execute)
    graph.add_node("extract_skills", SkillExtractorAgent().execute)
    graph.add_node("rag_search", RAGAgent().execute)
    graph.add_node("match_jd", JDMatcherAgent().execute)
    graph.add_node("build_resume", ResumeBuilderAgent().execute)

    graph.set_entry_point("parse_resume")
    graph.add_edge("parse_resume", "extract_skills")
    graph.add_edge("extract_skills", "rag_search")
    graph.add_edge("rag_search", "match_jd")
    graph.add_edge("match_jd", "build_resume")
    graph.add_edge("build_resume", END)

    return graph.compile()


resume_graph = build_resume_graph()
from langgraph.graph import StateGraph

from agents.resume_parser_agent import ResumeParserAgent
from agents.skill_extractor_agent import SkillExtractorAgent
from agents.rag_agent import RAGAgent
from agents.jd_matcher_agent import JDMatcherAgent
from agents.resume_builder_agent import ResumeBuilderAgent
from agents.evaluator_agent import EvaluatorAgent

from langgraph.states import ResumeState

builder = StateGraph(ResumeState)

builder.add_node(
    "resume_parser",
    ResumeParserAgent().execute
)

builder.add_node(
    "skill_extractor",
    SkillExtractorAgent().execute
)

builder.add_node(
    "rag",
    RAGAgent().execute
)

builder.add_node(
    "jd_match",
    JDMatcherAgent().execute
)

builder.add_node(
    "resume_builder",
    ResumeBuilderAgent().execute
)

builder.add_node(
    "evaluator",
    EvaluatorAgent().execute
)

builder.add_edge(
    "resume_parser",
    "skill_extractor"
)

builder.add_edge(
    "skill_extractor",
    "rag"
)

builder.add_edge(
    "rag",
    "jd_match"
)

builder.add_edge(
    "jd_match",
    "resume_builder"
)

builder.add_edge(
    "resume_builder",
    "evaluator"
)

graph = builder.compile()
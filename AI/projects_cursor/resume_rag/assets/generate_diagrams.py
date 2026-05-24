"""Generate architecture PNG diagrams (ASCII-safe)."""
from __future__ import annotations

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BG = "#0f172a"
CARD = "#1e293b"
BORDER = "#334155"
TEXT = "#f1f5f9"
MUTED = "#94a3b8"
BLUE = "#3b82f6"
PURPLE = "#8b5cf6"
GREEN = "#22c55e"
CYAN = "#06b6d4"
PINK = "#ec4899"


def box(ax, x, y, w, h, title, lines, color=BLUE, title_size=11):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        facecolor=CARD, edgecolor=color, linewidth=2,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h - 0.035, title, ha="center", va="top",
            fontsize=title_size, fontweight="bold", color=TEXT)
    for i, line in enumerate(lines):
        ax.text(x + 0.02, y + h - 0.075 - i * 0.035, line,
                ha="left", va="top", fontsize=8.5, color=MUTED)


def arrow(ax, x1, y1, x2, y2, color=CYAN):
    ax.add_patch(FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>", mutation_scale=12,
        color=color, linewidth=1.8,
    ))


def draw_architecture(path: str):
    fig, ax = plt.subplots(figsize=(16, 22), facecolor=BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Header
    header = FancyBboxPatch((0.03, 0.955), 0.94, 0.038, boxstyle="round,pad=0.01",
                            facecolor=PURPLE, edgecolor="none", alpha=0.9)
    ax.add_patch(header)
    ax.text(0.05, 0.978, "Agentic Resume AI Platform", fontsize=22, fontweight="bold", color="white")
    ax.text(0.05, 0.962, "Complete System Architecture and Application Flow", fontsize=11, color="#e0e7ff")
    ax.text(0.72, 0.978, "FastAPI + LangGraph + RAG + SSE/WebSocket", fontsize=11, color="white", ha="left")

    ax.text(0.05, 0.935, "01 - HIGH-LEVEL ARCHITECTURE", fontsize=10, fontweight="bold", color=CYAN)

    box(ax, 0.04, 0.78, 0.28, 0.14, "Streamlit Frontend :8501", [
        "Upload Resume (live agent timeline)",
        "Resume Analyzer | RAG Search | Dashboard",
        "Agent Runs | Resume Builder | Settings",
        "SSE stream via stream_api + agent_feed",
    ], BLUE)

    box(ax, 0.36, 0.78, 0.28, 0.14, "FastAPI Backend :8000", [
        "REST: /resumes /rag /agents /jobs",
        "SSE: /stream/analysis/{document_id}",
        "WebSocket: /ws/analysis/{document_id}",
        "Services: resume, rag, agent_events",
    ], PURPLE)

    box(ax, 0.68, 0.78, 0.28, 0.14, "RQ Worker (Background)", [
        "python -m app.jobs.worker",
        "LangGraph resume_graph.stream()",
        "Publishes agent.token events",
        "Saves AgentRun + ResumeAnalysis",
    ], GREEN)

    arrow(ax, 0.32, 0.85, 0.36, 0.85)
    ax.text(0.33, 0.855, "REST/SSE", fontsize=7, color=CYAN)
    arrow(ax, 0.64, 0.85, 0.68, 0.85)
    ax.text(0.645, 0.855, "RQ enqueue", fontsize=7, color=CYAN)

    ax.text(0.05, 0.755, "EXTERNAL SERVICES", fontsize=10, fontweight="bold", color=CYAN)
    services = [
        ("Groq LLM", "llama-3.3-70b"),
        ("OpenAI", "embeddings"),
        ("Pinecone", "vector search"),
        ("Redis", "queue + pub/sub"),
        ("SQL DB", "Snowflake/MySQL"),
        ("Storage", "PDF files"),
    ]
    for i, (t, s) in enumerate(services):
        x = 0.04 + (i % 3) * 0.31
        y = 0.68 - (i // 3) * 0.07
        box(ax, x, y, 0.28, 0.055, t, [s], BORDER)

    ax.text(0.05, 0.615, "02 - LANGGRAPH AGENT PIPELINE", fontsize=10, fontweight="bold", color=CYAN)
    agents = [
        ("1 Parser", "PyPDF -> text", "#0ea5e9"),
        ("2 Skills", "Groq stream", BLUE),
        ("3 RAG", "Pinecone", PURPLE),
        ("4 JD Match", "Groq stream", PINK),
        ("5 Builder", "Groq stream", GREEN),
        ("6 Index", "Pinecone upsert", CYAN),
    ]
    for i, (t, s, c) in enumerate(agents):
        x = 0.04 + i * 0.155
        box(ax, x, 0.52, 0.13, 0.075, t, [s], c)

    for i in range(5):
        arrow(ax, 0.04 + (i + 1) * 0.155 - 0.012, 0.557, 0.04 + (i + 1) * 0.155 + 0.02, 0.557, MUTED)

    ax.text(0.05, 0.495, "State: document_id | resume_text | skills_json | rag_context | jd_match_json | optimized_resume",
            fontsize=8, color=MUTED)

    ax.text(0.05, 0.465, "03 - REAL-TIME STREAMING (ChatGPT / Cursor style)", fontsize=10, fontweight="bold", color=CYAN)
    steps = [
        "Upload PDF", "Enqueue RQ", "Open SSE", "Worker runs",
        "Publish events", "UI timeline", "Complete",
    ]
    for i, s in enumerate(steps):
        x = 0.04 + i * 0.135
        c = GREEN if i == 6 else CARD
        ec = GREEN if i == 6 else CYAN
        box(ax, x, 0.38, 0.115, 0.065, s, [], ec)
        if i < 6:
            arrow(ax, x + 0.115, 0.412, x + 0.135, 0.412)

    ax.text(0.05, 0.355, "Events: pipeline.started | agent.started | agent.token | agent.progress | agent.completed | rag.indexed",
            fontsize=8, color=MUTED)

    ax.text(0.05, 0.325, "04 - DATA MODEL", fontsize=10, fontweight="bold", color=CYAN)
    box(ax, 0.04, 0.22, 0.28, 0.09, "ResumeDocument", ["document_id, file_name, status, content_text"], BLUE)
    box(ax, 0.36, 0.22, 0.28, 0.09, "ResumeAnalysis", ["skills_json, jd_match_json, optimized_resume"], PURPLE)
    box(ax, 0.68, 0.22, 0.28, 0.09, "AgentRun", ["agent_name, status, output_json per step"], GREEN)

    ax.text(0.05, 0.195, "Status: queued -> processing -> analyzed (or failed)", fontsize=9, color=GREEN)

    ax.text(0.05, 0.165, "05 - DEPLOYMENT (make run)", fontsize=10, fontweight="bold", color=CYAN)
    box(ax, 0.04, 0.06, 0.92, 0.09, "Local stack", [
        "redis-up | RQ worker | uvicorn :8000 | streamlit :8501",
        "Config: AI/.env | Dependencies: AI/pyproject.toml (uv sync)",
        "Docker Compose: api + worker + mysql + redis",
    ], BORDER)

    fig.savefig(path, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"Wrote {path}")


def draw_flow(path: str):
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    header = FancyBboxPatch((0.03, 0.91), 0.94, 0.06, boxstyle="round,pad=0.01",
                            facecolor=CYAN, edgecolor="none", alpha=0.85)
    ax.add_patch(header)
    ax.text(0.5, 0.945, "Application Flow - Upload to Analysis Complete", ha="center",
            fontsize=18, fontweight="bold", color="white")

    lanes = [
        ("USER / STREAMLIT", 0.78, [
            "Select PDF + JD", "Click Analyze", "Watch live feed", "See Groq tokens", "View results",
        ], BLUE),
        ("FASTAPI :8000", 0.58, [
            "POST /upload", "Enqueue RQ job", "SSE /stream/analysis", "Forward Redis events", "GET /resumes/{id}",
        ], PURPLE),
        ("RQ WORKER + LANGGRAPH", 0.32, [
            "Parser", "Skills (stream)", "RAG", "JD Match (stream)", "Builder (stream)", "Index + Save DB",
        ], GREEN),
        ("DATA STORES", 0.08, [
            "storage/resumes", "Redis queue+events", "SQL Database", "Pinecone vectors", "Groq + OpenAI APIs",
        ], BORDER),
    ]

    for label, y, items, color in lanes:
        ax.text(0.04, y + 0.11, label, fontsize=9, fontweight="bold", color=MUTED)
        patch = FancyBboxPatch((0.03, y), 0.94, 0.095, boxstyle="round,pad=0.01",
                               facecolor="#111827", edgecolor=BORDER, linewidth=1)
        ax.add_patch(patch)
        n = len(items)
        for i, item in enumerate(items):
            x = 0.05 + i * (0.88 / max(n - 1, 1)) if n > 1 else 0.05
            w = min(0.14, 0.88 / n - 0.01)
            box(ax, x, y + 0.02, w, 0.06, item, [], color)
            if i < n - 1:
                arrow(ax, x + w, y + 0.05, x + w + 0.02, y + 0.05, MUTED)

    # vertical flow hints
    arrow(ax, 0.12, 0.78, 0.12, 0.68, CYAN)
    arrow(ax, 0.35, 0.58, 0.35, 0.42, PURPLE)
    arrow(ax, 0.75, 0.32, 0.75, 0.17, GREEN)

    ax.text(0.5, 0.02, "Live events: agent.token streams Groq output to Streamlit timeline in real time",
            ha="center", fontsize=9, color=MUTED)

    fig.savefig(path, dpi=150, facecolor=BG, bbox_inches="tight", pad_inches=0.2)
    plt.close(fig)
    print(f"Wrote {path}")


if __name__ == "__main__":
    draw_architecture("architecture-diagram.png")
    draw_flow("application-flow.png")

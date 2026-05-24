AGENT_ORDER = [
    "parse_resume",
    "extract_skills",
    "rag_search",
    "match_jd",
    "build_resume",
]

AGENT_LABELS = {
    "parse_resume": "Resume Parser",
    "extract_skills": "Skill Extractor",
    "rag_search": "RAG Search",
    "match_jd": "JD Matcher",
    "build_resume": "Resume Builder",
    "rag_index": "Vector Index",
}

STATUS_ICON = {
    "pending": "⚪",
    "running": "🔄",
    "completed": "✅",
    "failed": "❌",
}


def _escape(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def init_agent_state() -> dict:
    return {
        agent: {
            "status": "pending",
            "label": AGENT_LABELS.get(agent, agent),
            "message": "Waiting…",
            "preview": None,
            "stream": None,
        }
        for agent in AGENT_ORDER
    }


def apply_event(state: dict, event: dict) -> dict:
    event_type = event.get("event", "")
    agent = event.get("agent")

    if event_type == "pipeline.started":
        state["_pipeline"] = {"status": "running", "message": event.get("message", "")}
    elif event_type == "agent.started" and agent:
        if agent not in state:
            state[agent] = {"label": event.get("label", agent), "message": "", "preview": None, "stream": None}
        state[agent]["status"] = "running"
        state[agent]["message"] = event.get("message", "Running…")
        state[agent]["stream"] = event.get("partial") or ""
    elif event_type == "agent.token" and agent:
        if agent not in state:
            state[agent] = {"label": event.get("label", agent), "message": "", "preview": None, "stream": None}
        state[agent]["status"] = "running"
        state[agent]["message"] = event.get("message", "Generating…")
        state[agent]["stream"] = event.get("partial", "")
    elif event_type == "agent.progress" and agent:
        if agent not in state:
            state[agent] = {"label": event.get("label", agent), "message": "", "preview": None, "stream": None}
        state[agent]["status"] = "running"
        state[agent]["message"] = event.get("message", "Working…")
        if event.get("partial") is not None:
            state[agent]["stream"] = event.get("partial", "")
    elif event_type == "agent.completed" and agent:
        if agent not in state:
            state[agent] = {"label": event.get("label", agent), "message": "", "preview": None, "stream": None}
        state[agent]["status"] = "completed"
        state[agent]["message"] = event.get("message", "Done")
        if event.get("preview"):
            state[agent]["preview"] = event["preview"]
            state[agent]["stream"] = event["preview"]
    elif event_type == "agent.failed" and agent:
        if agent not in state:
            state[agent] = {"label": event.get("label", agent), "message": "", "preview": None, "stream": None}
        state[agent]["status"] = "failed"
        state[agent]["message"] = event.get("message", "Failed")
    elif event_type == "rag.indexed":
        state["rag_index"] = {
            "status": "completed",
            "label": event.get("label", "Vector Index"),
            "message": event.get("message", "Indexed"),
            "preview": None,
            "stream": None,
        }
    elif event_type in {"pipeline.completed", "pipeline.failed"}:
        state["_pipeline"] = {
            "status": "completed" if event_type == "pipeline.completed" else "failed",
            "message": event.get("message", ""),
        }

    state["_last_event"] = event
    return state


def render_timeline_html(state: dict) -> str:
    pipeline = state.get("_pipeline", {})
    pipeline_status = pipeline.get("status", "running")
    pipeline_msg = pipeline.get("message", "Agent pipeline")

    rows = []
    for agent in AGENT_ORDER:
        info = state.get(agent, {})
        status = info.get("status", "pending")
        icon = STATUS_ICON.get(status, "⚪")
        label = info.get("label", AGENT_LABELS.get(agent, agent))
        message = info.get("message", "")
        preview = info.get("preview")
        stream = info.get("stream")

        status_class = f"agent-{status}"
        preview_html = ""

        if stream and status == "running":
            safe = _escape(str(stream)[-1800:])
            preview_html = (
                f'<div class="agent-preview agent-stream">{safe}'
                f'<span class="cursor">▍</span></div>'
            )
        elif preview and status == "completed":
            safe = _escape(str(preview))
            preview_html = f'<div class="agent-preview">{safe}</div>'

        rows.append(
            f"""
            <div class="agent-step {status_class}">
                <div class="agent-icon">{icon}</div>
                <div class="agent-body">
                    <div class="agent-title">{label}</div>
                    <div class="agent-message">{_escape(message)}</div>
                    {preview_html}
                </div>
            </div>
            """
        )

    if "rag_index" in state:
        info = state["rag_index"]
        rows.append(
            f"""
            <div class="agent-step agent-completed">
                <div class="agent-icon">✅</div>
                <div class="agent-body">
                    <div class="agent-title">{info.get('label')}</div>
                    <div class="agent-message">{_escape(info.get('message', ''))}</div>
                </div>
            </div>
            """
        )

    pipeline_icon = STATUS_ICON.get(pipeline_status, "🔄")

    return f"""
    <style>
    .agent-panel {{
        font-family: ui-sans-serif, system-ui, -apple-system, sans-serif;
        border: 1px solid rgba(128,128,128,0.35);
        border-radius: 12px;
        padding: 16px;
        background: rgba(128,128,128,0.08);
    }}
    .agent-header {{
        display: flex; align-items: center; gap: 10px;
        margin-bottom: 14px; font-weight: 600;
    }}
    .agent-step {{
        display: flex; gap: 12px; padding: 10px 0;
        border-left: 2px solid rgba(128,128,128,0.25);
        margin-left: 12px; padding-left: 16px;
    }}
    .agent-step.agent-running {{ border-left-color: #3b82f6; }}
    .agent-step.agent-completed {{ border-left-color: #22c55e; }}
    .agent-step.agent-failed {{ border-left-color: #ef4444; }}
    .agent-icon {{ font-size: 1.1rem; min-width: 24px; }}
    .agent-title {{ font-weight: 600; font-size: 0.95rem; }}
    .agent-message {{ color: rgba(128,128,128,0.95); font-size: 0.85rem; margin-top: 2px; }}
    .agent-preview {{
        margin-top: 8px; padding: 8px 10px;
        background: rgba(128,128,128,0.12);
        border-radius: 8px; font-size: 0.8rem;
        white-space: pre-wrap; line-height: 1.4;
        font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    }}
    .agent-stream {{
        max-height: 240px; overflow-y: auto;
        border: 1px solid rgba(59,130,246,0.35);
    }}
    .cursor {{
        animation: blink 1s step-end infinite;
        color: #3b82f6; font-weight: bold;
    }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    </style>
    <div class="agent-panel">
        <div class="agent-header">{pipeline_icon} {_escape(pipeline_msg)}</div>
        {''.join(rows)}
    </div>
    """


def render_live_log(events: list[dict]) -> str:
    lines = []
    for event in events[-20:]:
        if event.get("event") in {"ping", "agent.token"}:
            continue
        label = event.get("label") or event.get("agent") or event.get("event")
        message = event.get("message", "")
        if event.get("event") == "agent.progress":
            partial = event.get("partial")
            if partial:
                message = f"{message} · {len(partial)} chars"
        lines.append(f"• **{label}** — {message}")
    return "\n".join(lines)


def live_output_markdown(event: dict) -> str | None:
    if event.get("event") not in {"agent.token", "agent.progress", "agent.completed"}:
        return None
    partial = event.get("partial") or event.get("preview")
    if not partial:
        return None
    label = event.get("label", "Agent")
    live = " (live)" if event.get("event") in {"agent.token", "agent.progress"} else ""
    return f"**{label}**{live}\n\n```\n{partial[-8000:]}\n```"

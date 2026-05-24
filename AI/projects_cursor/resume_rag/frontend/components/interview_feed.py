import json
import re

INTERVIEW_AGENT_ORDER = [
    "load_context",
    "generate_questions",
    "format_output",
]

INTERVIEW_LABELS = {
    "load_context": "Context Loader",
    "generate_questions": "Question Generator",
    "format_output": "Response Formatter",
}

STATUS_ICON = {
    "pending": "⚪",
    "running": "🔄",
    "completed": "✅",
    "failed": "❌",
}

DIFFICULTY_COLORS = {
    "easy": "#22c55e",
    "medium": "#f59e0b",
    "hard": "#ef4444",
}


def init_interview_state() -> dict:
    return {
        agent: {
            "status": "pending",
            "label": INTERVIEW_LABELS.get(agent, agent),
            "message": "Waiting…",
            "stream": None,
        }
        for agent in INTERVIEW_AGENT_ORDER
    }


def apply_interview_event(state: dict, event: dict) -> dict:
    event_type = event.get("event", "")
    agent = event.get("agent")

    if event_type == "pipeline.started":
        state["_pipeline"] = {"status": "running", "message": event.get("message", "")}
    elif event_type == "agent.started" and agent:
        state[agent]["status"] = "running"
        state[agent]["message"] = event.get("message", "Running…")
        state[agent]["stream"] = ""
    elif event_type in {"agent.token", "agent.progress"} and agent:
        state[agent]["status"] = "running"
        state[agent]["message"] = event.get("message", "Working…")
        if event.get("partial"):
            state[agent]["stream"] = event["partial"]
    elif event_type == "agent.completed" and agent:
        state[agent]["status"] = "completed"
        state[agent]["message"] = event.get("message", "Done")
        if event.get("preview"):
            state[agent]["stream"] = event["preview"]
        if event.get("questions"):
            state["_questions"] = event["questions"]
    elif event_type == "pipeline.completed":
        state["_pipeline"] = {
            "status": "completed",
            "message": event.get("message", "Complete"),
        }
        if event.get("questions"):
            state["_questions"] = event["questions"]
    elif event_type == "pipeline.failed":
        state["_pipeline"] = {"status": "failed", "message": event.get("message", "Failed")}

    state["_last_event"] = event
    return state


def render_pipeline_steps(state: dict) -> None:
    import streamlit as st

    pipeline = state.get("_pipeline", {})
    pipeline_status = pipeline.get("status", "running")
    pipeline_msg = pipeline.get("message", "Interview pipeline")
    pipeline_icon = STATUS_ICON.get(pipeline_status, "🔄")

    st.caption(f"{pipeline_icon} {pipeline_msg}")

    for agent in INTERVIEW_AGENT_ORDER:
        info = state.get(agent, {})
        status = info.get("status", "pending")
        icon = STATUS_ICON.get(status, "⚪")
        label = info.get("label", agent)
        message = info.get("message", "")

        if status == "failed":
            st.error(f"{icon} **{label}** — {message}")
        elif status == "running":
            st.markdown(f"{icon} **{label}** — _{message}_")
        elif status == "completed":
            st.markdown(f"{icon} **{label}** — {message}")
        else:
            st.markdown(f"{icon} {label} — waiting")


def render_activity_scroll(state: dict) -> None:
    import streamlit as st

    st.markdown("🔄 **Generating — live progress**")

    pipeline = state.get("_pipeline", {})
    if pipeline.get("message"):
        st.markdown(pipeline["message"])

    for agent in INTERVIEW_AGENT_ORDER:
        info = state.get(agent, {})
        status = info.get("status", "pending")
        if status == "pending":
            continue
        icon = STATUS_ICON.get(status, "⚪")
        label = info.get("label", agent)
        message = info.get("message", "")
        st.markdown(f"{icon} **{label}** — {message}")

    stream = (state.get("generate_questions") or {}).get("stream") or ""
    if stream:
        st.caption(f"LLM output: {len(stream):,} chars received…")
    else:
        st.caption("Waiting for Groq stream…")

    st.markdown(":blue[▍]")


def render_questions_cards(questions: list[dict]) -> None:
    import streamlit as st

    if not questions:
        st.warning("No questions were generated.")
        return

    st.markdown(f"### ✅ {len(questions)} tailored interview questions")

    for q in questions:
        diff = str(q.get("difficulty", "Medium"))
        color = DIFFICULTY_COLORS.get(diff.lower(), "#64748b")
        num = q.get("number", "")
        category = q.get("category", "General")
        question = q.get("question", "")
        focus = q.get("focus", "")

        with st.expander(f"Q{num} · {category} · {diff}", expanded=True):
            st.markdown(
                f"<span style='color:{color};font-weight:600'>{diff}</span>",
                unsafe_allow_html=True,
            )
            st.markdown(question)
            if focus:
                st.caption(f"🎯 Focus: {focus}")


def render_idle_placeholder() -> None:
    import streamlit as st

    st.info(
        "Enter skills and click **Generate Interview Questions**. "
        "Results will appear here when the pipeline completes."
    )

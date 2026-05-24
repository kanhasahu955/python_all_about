import streamlit as st


def render_metrics(counts: dict) -> None:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Resumes", counts.get("total", 0))
    col2.metric("Analyzed", counts.get("analyzed", 0))
    col3.metric("In queue", counts.get("queued", 0))
    col4.metric("Failed", counts.get("failed", 0))


def render_queue_hint(counts: dict) -> None:
    queued = counts.get("queued", 0)
    if queued:
        st.info(
            f"{queued} resume(s) still processing. "
            "Use **Retry** below if stuck, or restart with `make stop && make run`."
        )


def render_resume_table(resumes: list[dict]) -> None:
    if resumes:
        st.dataframe(resumes, width="stretch")

import streamlit as st

from components.dashboard_live import render_metrics, render_queue_hint, render_resume_table
from services.resume_api import ResumeApi
from services.stream_api import StreamApi


def _render_retry_section(resumes: list[dict]) -> None:
    st.subheader("Retry analysis")
    retry_candidates = [
        r
        for r in resumes
        if r.get("status") in ("queued", "processing", "failed")
    ]
    if not retry_candidates:
        st.caption("No resumes need retry.")
        return

    for r in retry_candidates:
        cols = st.columns([4, 1])
        file_ok = r.get("file_exists", True)
        missing = "" if file_ok else " · ⚠️ PDF missing — re-upload instead"
        cols[0].caption(
            f"`{r['document_id'][:8]}…` · {r['file_name']} · **{r['status']}**{missing}"
        )
        if not file_ok:
            cols[1].caption("N/A")
            continue
        if cols[1].button("Retry", key=f"retry_{r['document_id']}"):
            try:
                result = ResumeApi.retry_analysis(r["document_id"])
                st.success(f"Re-queued · job `{result.get('job_id', '—')[:8]}…`")
                st.session_state.pop("_dashboard_resumes", None)
            except Exception as exc:
                st.error(str(exc))


st.title("Dashboard")

live = st.toggle(
    "Live updates (SSE stream)",
    value=True,
    help="Updates metrics and table in place — no full page reload.",
)

if live:
    st.caption("SSE: `/api/v1/stream/dashboard` — updates in place when pipelines run")

# Retry controls stay above the stream so buttons remain clickable.
initial = st.session_state.get("_dashboard_resumes")
if initial is None:
    try:
        initial = ResumeApi.list_resumes()
        st.session_state["_dashboard_resumes"] = initial
    except Exception:
        initial = []

_render_retry_section(initial or [])

st.divider()

metrics_slot = st.empty()
hint_slot = st.empty()
table_header = st.empty()
table_slot = st.empty()

try:
    if live:
        for event in StreamApi.stream_dashboard():
            if event.get("event") != "snapshot":
                continue

            counts = event.get("counts", {})
            resumes = event.get("resumes", [])
            st.session_state["_dashboard_resumes"] = resumes

            with metrics_slot.container():
                render_metrics(counts)

            with hint_slot.container():
                render_queue_hint(counts)

            table_header.subheader("All resumes")
            with table_slot.container():
                render_resume_table(resumes)
    else:
        resumes = ResumeApi.list_resumes()
        st.session_state["_dashboard_resumes"] = resumes

        analyzed = sum(1 for r in resumes if r.get("status") == "analyzed")
        queued = sum(1 for r in resumes if r.get("status") in ("queued", "processing"))
        failed = sum(1 for r in resumes if r.get("status") == "failed")
        counts = {
            "total": len(resumes),
            "analyzed": analyzed,
            "queued": queued,
            "failed": failed,
        }

        with metrics_slot.container():
            render_metrics(counts)
        with hint_slot.container():
            render_queue_hint(counts)
        table_header.subheader("All resumes")
        with table_slot.container():
            render_resume_table(resumes)

        if st.button("Refresh"):
            st.session_state.pop("_dashboard_resumes", None)
            st.rerun()

except Exception as exc:
    st.error(f"Could not load dashboard: {exc}")

import json

import streamlit as st

from components.agent_feed import (
    apply_event,
    init_agent_state,
    live_output_markdown,
    render_live_log,
    render_timeline_html,
)
from services.agent_api import AgentApi
from services.resume_api import ResumeApi
from services.stream_api import StreamApi

st.title("Agent Runs")

tab_history, tab_live = st.tabs(["History", "Live monitor"])

with tab_history:
    try:
        resumes = ResumeApi.list_resumes()
    except Exception as exc:
        st.error(f"Could not load resumes: {exc}")
        resumes = []

    document_options = ["All resumes"] + [
        f"{r['file_name']} ({r['document_id'][:8]}…)" for r in resumes
    ]
    selected = st.selectbox("Filter by resume", document_options, key="hist_filter")

    document_id = None
    if selected != "All resumes":
        idx = document_options.index(selected) - 1
        document_id = resumes[idx]["document_id"]

    if st.button("Refresh history"):
        st.rerun()

    try:
        runs = AgentApi.list_runs(document_id=document_id)
        if not runs:
            st.info("No agent runs yet. Upload a resume to trigger the LangGraph pipeline.")
        else:
            st.dataframe(
                [
                    {
                        "agent": run.get("agent"),
                        "status": run.get("status"),
                        "document_id": run.get("document_id"),
                        "run_id": run.get("run_id"),
                    }
                    for run in runs
                ],
                width="stretch",
            )

            st.subheader("Run details")
            for run in runs[:10]:
                with st.expander(f"{run.get('agent')} — {run.get('status')} (#{run.get('run_id', '')[:8]})"):
                    st.caption(f"Document: `{run.get('document_id')}`")
                    output = run.get("output_json")
                    if output:
                        try:
                            st.json(json.loads(output))
                        except (json.JSONDecodeError, TypeError):
                            st.text(str(output)[:5000])
    except Exception as exc:
        st.error(f"Could not load agent runs: {exc}")

with tab_live:
    st.caption("Watch agents run in real time — like Cursor / ChatGPT tool steps.")

    try:
        live_resumes = ResumeApi.list_resumes()
    except Exception:
        live_resumes = []

    live_doc_id = st.text_input("Document ID to watch")
    if live_resumes:
        pick = st.selectbox(
            "Or pick a resume",
            ["—"] + [f"{r['file_name']} ({r['status']})" for r in live_resumes],
            key="live_pick",
        )
        if pick != "—":
            live_doc_id = live_resumes[[f"{r['file_name']} ({r['status']})" for r in live_resumes].index(pick)][
                "document_id"
            ]

    if st.button("Start live stream", type="primary"):
        if not live_doc_id.strip():
            st.error("Enter a document ID.")
        else:
            doc_id = live_doc_id.strip()
            st.caption(f"WebSocket: `{StreamApi.websocket_url(doc_id)}`")

            timeline = st.empty()
            log_box = st.empty()
            preview_box = st.empty()
            state = init_agent_state()
            events: list[dict] = []

            with st.spinner("Connecting to agent stream…"):
                for event in StreamApi.stream_analysis(doc_id):
                    events.append(event)
                    state = apply_event(state, event)
                    timeline.markdown(render_timeline_html(state), unsafe_allow_html=True)
                    log_box.markdown(render_live_log(events))

                    live_md = live_output_markdown(event)
                    if live_md:
                        preview_box.markdown(live_md)

                    if event.get("event") in {"pipeline.completed", "pipeline.failed"}:
                        if event.get("event") == "pipeline.completed":
                            st.success("Pipeline finished.")
                        else:
                            st.error("Pipeline failed.")
                        break

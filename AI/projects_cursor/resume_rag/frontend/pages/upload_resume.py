import streamlit as st

from components.agent_feed import (
    apply_event,
    init_agent_state,
    live_output_markdown,
    render_live_log,
    render_timeline_html,
)
from services.resume_api import ResumeApi
from services.stream_api import StreamApi

st.title("Upload Resume")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
jd = st.text_area("Job Description (optional)")

if st.button("Analyze Resume", type="primary"):
    if not uploaded_file:
        st.error("Please upload a PDF resume.")
    else:
        try:
            with st.spinner("Uploading…"):
                result = ResumeApi.upload_resume(uploaded_file, jd)

            document_id = result.get("document_id")
            status = result.get("status")

            if not document_id:
                st.error("Upload failed — no document ID returned.")
                st.stop()

            st.success(f"Uploaded · Document `{document_id[:8]}…` · Status: **{status}**")

            st.subheader("Live agent activity")
            st.caption(
                f"SSE stream · WebSocket: `{StreamApi.websocket_url(document_id)}`"
            )

            timeline = st.empty()
            log_box = st.empty()
            preview_box = st.empty()

            state = init_agent_state()
            events: list[dict] = []

            for event in StreamApi.stream_analysis(document_id):
                events.append(event)
                state = apply_event(state, event)
                timeline.markdown(render_timeline_html(state), unsafe_allow_html=True)
                log_box.markdown(render_live_log(events))

                live_md = live_output_markdown(event)
                if live_md:
                    preview_box.markdown(live_md)

                if event.get("event") in {"pipeline.completed", "pipeline.failed"}:
                    break

            final = ResumeApi.get_resume(document_id)
            last_event = events[-1] if events else {}
            if final.get("status") == "analyzed":
                st.success("Analysis complete — open **Resume Analyzer** for full results.")
            elif last_event.get("event") == "pipeline.failed":
                st.error("Pipeline failed. Check logs above.")

        except Exception as exc:
            st.error(f"Upload or analysis failed: {exc}")

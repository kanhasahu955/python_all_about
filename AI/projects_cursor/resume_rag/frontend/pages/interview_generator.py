import streamlit as st

from components.interview_feed import (
    apply_interview_event,
    init_interview_state,
    render_activity_scroll,
    render_idle_placeholder,
    render_pipeline_steps,
    render_questions_cards,
)
from services.resume_api import ResumeApi
from services.stream_api import StreamApi

if "iv_questions" not in st.session_state:
    st.session_state.iv_questions = []
if "iv_pipeline_state" not in st.session_state:
    st.session_state.iv_pipeline_state = None
if "iv_error" not in st.session_state:
    st.session_state.iv_error = None

st.markdown(
    """
    <style>
    .main-header {
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    .sub-head { color: #64748b; margin-bottom: 1.5rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<p class="main-header">Interview Question Generator</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-head">Pipeline on the right · formatted questions below when complete.</p>',
    unsafe_allow_html=True,
)

col_form, col_pipeline = st.columns([1, 1], gap="large")

with col_form:
    st.subheader("Input")
    try:
        resumes = ResumeApi.list_resumes()
    except Exception:
        resumes = []

    document_id = None
    if resumes:
        options = ["Skills only (no resume)"] + [
            f"{r['file_name']}  ·  {r['status']}" for r in resumes
        ]
        picked = st.selectbox("Resume source", options, help="Pick an analyzed resume to personalize questions")
        if picked != "Skills only (no resume)":
            document_id = resumes[options.index(picked) - 1]["document_id"]
            picked_status = resumes[options.index(picked) - 1]["status"]
            if picked_status != "analyzed":
                st.warning(
                    f"Selected resume status is **{picked_status}**. "
                    "Enter skills below or wait for analysis to finish."
                )
            elif not st.session_state.get("interview_skills"):
                try:
                    detail = ResumeApi.get_resume(document_id)
                    skills_from_resume = (detail.get("analysis") or {}).get("skills_json")
                    if skills_from_resume:
                        st.session_state.interview_skills = skills_from_resume
                except Exception:
                    pass

    skills = st.text_area(
        "Skills & focus areas",
        height=140,
        placeholder="e.g. Python, FastAPI, LangGraph, Snowflake, system design…",
        key="interview_skills",
    )

    btn_col1, btn_col2 = st.columns(2)
    generate = btn_col1.button("Generate Interview Questions", type="primary", use_container_width=True)
    if btn_col2.button("Clear results", use_container_width=True):
        st.session_state.iv_questions = []
        st.session_state.iv_pipeline_state = None
        st.session_state.iv_error = None
        st.rerun()

with col_pipeline:
    st.subheader("Agent pipeline")
    pipeline_slot = st.empty()

st.divider()
st.subheader("Generated questions")
questions_slot = st.empty()

if generate:
    st.session_state.iv_questions = []
    st.session_state.iv_pipeline_state = None
    st.session_state.iv_error = None

    if not skills.strip() and not document_id:
        st.session_state.iv_error = "Enter skills or select a resume."
    else:
        try:
            with st.spinner("Starting interview pipeline…"):
                start = StreamApi.start_interview(skills=skills, document_id=document_id)
                session_id = start["session_id"]

            state = init_interview_state()
            questions: list = []

            with pipeline_slot.container():
                render_pipeline_steps(state)
            with questions_slot.container():
                st.caption("Streaming from Groq…")
                render_activity_scroll(state)

            for event in StreamApi.stream_interview(session_id):
                state = apply_interview_event(state, event)
                st.session_state.iv_pipeline_state = state

                with pipeline_slot.container():
                    render_pipeline_steps(state)

                pipeline_status = state.get("_pipeline", {}).get("status", "running")

                if pipeline_status == "failed":
                    st.session_state.iv_error = state["_pipeline"].get("message", "Generation failed")
                    with questions_slot.container():
                        st.error(st.session_state.iv_error)
                    break

                if pipeline_status != "completed":
                    with questions_slot.container():
                        render_activity_scroll(state)
                    continue

                questions = event.get("questions") or state.get("_questions") or []
                break

            if questions:
                st.session_state.iv_questions = questions
                st.session_state.iv_error = None
            elif not st.session_state.iv_error:
                st.session_state.iv_error = "Pipeline finished but no questions were parsed."

        except Exception as exc:
            st.session_state.iv_error = str(exc)

# Persisted display (survives Streamlit reruns)
if st.session_state.iv_error:
    with questions_slot.container():
        st.error(st.session_state.iv_error)

elif st.session_state.iv_questions:
    with pipeline_slot.container():
        if st.session_state.iv_pipeline_state:
            render_pipeline_steps(st.session_state.iv_pipeline_state)
    with questions_slot.container():
        render_questions_cards(st.session_state.iv_questions)

elif st.session_state.iv_pipeline_state:
    with pipeline_slot.container():
        render_pipeline_steps(st.session_state.iv_pipeline_state)
    with questions_slot.container():
        render_activity_scroll(st.session_state.iv_pipeline_state)

else:
    with pipeline_slot.container():
        st.info("Pipeline steps appear here when you generate.")
    with questions_slot.container():
        render_idle_placeholder()

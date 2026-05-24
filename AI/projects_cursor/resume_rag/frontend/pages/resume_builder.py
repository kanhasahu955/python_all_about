import streamlit as st

from components.resume_editor import render_download_bar, render_editor_preview
from services.resume_api import ResumeApi
from services.stream_api import StreamApi

if "rb_content" not in st.session_state:
    st.session_state.rb_content = ""
if "rb_source_id" not in st.session_state:
    st.session_state.rb_source_id = None
if "rb_error" not in st.session_state:
    st.session_state.rb_error = None

st.markdown(
    """
    <style>
    .rb-header {
        background: linear-gradient(90deg, #059669, #2563eb);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
    }
    .rb-sub { color: #64748b; margin-bottom: 1rem; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<p class="rb-header">Resume Builder</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="rb-sub">ATS-optimized rewrite · live Groq stream · edit & download as Word or Markdown</p>',
    unsafe_allow_html=True,
)

col_input, col_output = st.columns([1, 1.2], gap="large")

analyzed: list = []
try:
    resumes = ResumeApi.list_resumes()
    analyzed = [r for r in resumes if r.get("status") == "analyzed"]
except Exception:
    analyzed = []

with col_input:
    st.subheader("Source & target")

    source_options = ["Paste manually"] + [f"{r['file_name']}" for r in analyzed]
    picked = st.selectbox("Load from analyzed resume", source_options)

    if picked != "Paste manually":
        idx = source_options.index(picked) - 1
        doc_id = analyzed[idx]["document_id"]
        if st.session_state.rb_source_id != doc_id:
            try:
                detail = ResumeApi.get_resume(doc_id)
                st.session_state.rb_source_id = doc_id
                st.session_state.rb_source_text = detail.get("content_text") or ""
                analysis = detail.get("analysis") or {}
                if analysis.get("optimized_resume") and not st.session_state.rb_content:
                    st.session_state.rb_content = analysis["optimized_resume"]
            except Exception as exc:
                st.warning(f"Could not load resume: {exc}")
    else:
        st.session_state.rb_source_id = None

    if "rb_source_text" not in st.session_state:
        st.session_state.rb_source_text = ""

    source_text = st.text_area(
        "Original resume text",
        value=st.session_state.rb_source_text,
        height=200,
        placeholder="Paste resume text or pick an analyzed upload…",
        key="rb_source_text_area",
    )
    st.session_state.rb_source_text = source_text

    job_description = st.text_area(
        "Target job description",
        height=160,
        placeholder="Paste the job posting — keywords will be woven into the rewrite…",
        key="rb_jd",
    )

    btn_gen, btn_clear, btn_load = st.columns(3)
    generate = btn_gen.button("✨ Generate", type="primary", use_container_width=True)
    if btn_clear.button("Clear", use_container_width=True):
        st.session_state.rb_content = ""
        st.session_state.rb_error = None
        st.rerun()
    if btn_load.button("Load saved", use_container_width=True) and st.session_state.rb_source_id:
        try:
            detail = ResumeApi.get_resume(st.session_state.rb_source_id)
            saved = (detail.get("analysis") or {}).get("optimized_resume")
            if saved:
                st.session_state.rb_content = saved
                st.session_state["rb_editor_body"] = saved
                st.session_state.rb_error = None
                st.rerun()
            else:
                st.info("No saved optimized resume for this document yet.")
        except Exception as exc:
            st.error(str(exc))

with col_output:
    st.subheader("Editor & preview")
    preview_slot = st.empty()
    status_slot = st.empty()

if generate:
    st.session_state.rb_error = None
    if not source_text.strip():
        st.session_state.rb_error = "Enter original resume text or load an analyzed resume."
    else:
        try:
            with status_slot.container():
                status = st.status("Streaming optimized resume from Groq…", expanded=True)
            chunks: list[str] = []
            document_id = st.session_state.rb_source_id

            for token in StreamApi.stream_build(
                resume_text=source_text,
                job_description=job_description,
                document_id=document_id,
            ):
                chunks.append(token)
                live = "".join(chunks)
                with preview_slot.container():
                    st.caption("Live stream…")
                    st.markdown(live)
                st.session_state.rb_content = live

            st.session_state.rb_content = "".join(chunks)
            st.session_state["rb_editor_body"] = st.session_state.rb_content
            status.update(label="Resume generated", state="complete", expanded=False)
        except Exception as exc:
            st.session_state.rb_error = str(exc)
            try:
                result = ResumeApi.build_resume(
                    source_text,
                    job_description,
                    document_id=st.session_state.rb_source_id,
                )
                st.session_state.rb_content = result.get("optimized_resume", "")
                st.session_state["rb_editor_body"] = st.session_state.rb_content
                with status_slot.container():
                    st.info("Used non-streaming API fallback.")
            except Exception as inner:
                st.session_state.rb_error = str(inner or exc)

if st.session_state.rb_error:
    st.error(st.session_state.rb_error)

if st.session_state.rb_content:
    with col_output:
        edited = render_editor_preview(st.session_state.rb_content, editor_key="rb_editor_body")
        st.session_state.rb_content = edited
        file_stem = "optimized_resume"
        if st.session_state.rb_source_id:
            for r in analyzed:
                if r["document_id"] == st.session_state.rb_source_id:
                    file_stem = r["file_name"].rsplit(".", 1)[0] + "_optimized"
                    break
        render_download_bar(edited, file_stem=file_stem)
elif not generate:
    with col_output:
        preview_slot.info(
            "Your optimized resume appears here with **Editor** and **Preview** tabs. "
            "Generate to start, then download as `.docx`, `.md`, or `.txt`."
        )

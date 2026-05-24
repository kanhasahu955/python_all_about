import streamlit as st

from services.resume_api import ResumeApi
from services.stream_api import StreamApi

st.title("Resume Builder")

resume = st.text_area("Resume text", height=250, placeholder="Paste resume content or extracted text…")
target_role = st.text_area("Target role / job description", height=150)

if st.button("Generate Resume", type="primary"):
    if not resume.strip():
        st.error("Enter resume text.")
    else:
        prompt = f"""Optimize this resume for the target job. Return markdown only.

Job Description:
{target_role}

Resume:
{resume}
"""
        output = st.empty()
        status = st.status("Generating with Groq (streaming)…", expanded=True)
        chunks: list[str] = []

        try:
            for token in StreamApi.stream_llm(prompt):
                chunks.append(token)
                output.markdown("".join(chunks))
            status.update(label="Done", state="complete", expanded=False)
        except Exception as exc:
            status.update(label="Failed", state="error")
            try:
                result = ResumeApi.build_resume(resume, target_role)
                output.markdown(result.get("optimized_resume", ""))
                st.info("Fell back to non-streaming API.")
            except Exception as inner:
                st.error(f"Generation failed: {inner or exc}")

st.divider()
st.caption("Tip: analyze a PDF on **Upload Resume** and watch agents live during processing.")

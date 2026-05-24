import json

import streamlit as st

from services.resume_api import ResumeApi

st.title("Resume Analyzer")

try:
    resumes = ResumeApi.list_resumes()
except Exception as exc:
    st.error(f"Could not load resumes: {exc}")
    resumes = []

document_id = None
if resumes:
    options = {f"{r['file_name']} ({r['status']})": r["document_id"] for r in resumes}
    picked = st.selectbox("Select resume", list(options.keys()))
    document_id = options[picked]

manual_id = st.text_input("Or enter document ID", value=document_id or "")
if manual_id:
    document_id = manual_id

if st.button("Get Analysis", type="primary"):
    if not document_id:
        st.error("Select or enter a document ID.")
    else:
        try:
            result = ResumeApi.get_resume(document_id)
            st.subheader(result["file_name"])
            st.write(f"Status: **{result['status']}**")

            analysis = result.get("analysis") or {}
            for key in ("skills_json", "jd_match_json", "optimized_resume", "interview_questions"):
                value = analysis.get(key)
                if not value:
                    continue
                st.subheader(key.replace("_", " ").title())
                try:
                    st.json(json.loads(value))
                except (json.JSONDecodeError, TypeError):
                    st.markdown(value)

            if result.get("content_text"):
                with st.expander("Extracted resume text"):
                    st.text(result["content_text"][:5000])
        except Exception as exc:
            st.error(f"Could not load analysis: {exc}")

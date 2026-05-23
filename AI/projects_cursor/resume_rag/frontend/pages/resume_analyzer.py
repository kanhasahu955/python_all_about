import json

import streamlit as st

from services.resume_api import ResumeApi

st.title("Resume Analyzer")

document_id = st.text_input("Document ID")

if st.button("Get Analysis"):
    if not document_id:
        st.error("Enter a document ID.")
    else:
        try:
            result = ResumeApi.get_resume(document_id)
            st.subheader(result["file_name"])
            st.write(f"Status: **{result['status']}**")

            analysis = result.get("analysis") or {}
            for key in ("skills_json", "jd_match_json", "optimized_resume"):
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

import streamlit as st

from services.resume_api import ResumeApi

st.title("Dashboard")

try:
    resumes = ResumeApi.list_resumes()
    analyzed = sum(1 for r in resumes if r.get("status") == "analyzed")
    queued = sum(1 for r in resumes if r.get("status") in ("queued", "processing"))

    col1, col2, col3 = st.columns(3)
    col1.metric("Resumes", len(resumes))
    col2.metric("Analyzed", analyzed)
    col3.metric("In queue", queued)

    if resumes:
        st.subheader("All resumes")
        st.dataframe(resumes, use_container_width=True)
except Exception as exc:
    st.error(f"Could not load dashboard: {exc}")

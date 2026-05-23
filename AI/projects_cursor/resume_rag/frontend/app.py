import streamlit as st

from components.sidebar import render_sidebar
from services.resume_api import ResumeApi

st.set_page_config(page_title="Resume AI", page_icon="🤖", layout="wide")

render_sidebar()

st.title("🤖 Agentic Resume Platform")
st.write(
    """
Welcome! Use the sidebar pages to:

- **Upload Resume** — upload a PDF and optional job description
- **Resume Analyzer** — view analysis results by document ID
- **RAG Search** — semantic search over indexed resumes
- **Dashboard** — overview stats
"""
)

try:
    resumes = ResumeApi.list_resumes()
    st.metric("Total resumes", len(resumes))
    if resumes:
        st.subheader("Recent uploads")
        st.dataframe(resumes, use_container_width=True)
except Exception as exc:
    st.warning(f"Backend not reachable: {exc}. Start API with `uvicorn app.main:app --reload`")

import streamlit as st

st.title(
    "Resume Analyzer"
)

document_id = st.text_input(
    "Document ID"
)

if st.button(
    "Get Analysis"
):

    st.json(
        {
            "score": 89,
            "ats": 92,
            "missing_skills": [
                "LangGraph",
                "Databricks"
            ]
        }
    )
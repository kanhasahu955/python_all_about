import streamlit as st

st.title(
    "Dashboard"
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Resumes",
    120
)

col2.metric(
    "Analyses",
    90
)

col3.metric(
    "Interviews",
    56
)

col4.metric(
    "RAG Docs",
    5000
)
import streamlit as st

st.title(
    "Interview Generator"
)

skills = st.text_area(
    "Skills"
)

if st.button(
    "Generate Questions"
):

    st.write(
        """
        1. Explain FastAPI

        2. Explain LangGraph

        3. Explain Pinecone
        """
    )
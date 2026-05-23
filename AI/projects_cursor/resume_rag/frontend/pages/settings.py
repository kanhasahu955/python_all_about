import streamlit as st

st.title(
    "Settings"
)

openai_key = st.text_input(
    "OpenAI Key",
    type="password"
)

pinecone_key = st.text_input(
    "Pinecone Key",
    type="password"
)

langfuse_key = st.text_input(
    "Langfuse Key",
    type="password"
)

if st.button(
    "Save"
):

    st.success(
        "Saved"
    )
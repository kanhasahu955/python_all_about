import streamlit as st

st.title(
    "RAG Search"
)

query = st.text_input(
    "Search"
)

if st.button(
    "Search"
):

    st.write(
        """
        Resume Result 1

        Resume Result 2
        """
    )
import streamlit as st

from services.rag_api import RagApi

st.title("RAG Search")

query = st.text_input("Search resumes")
top_k = st.slider("Results", min_value=1, max_value=20, value=5)

if st.button("Search"):
    if not query:
        st.error("Enter a search query.")
    else:
        try:
            result = RagApi.search(query, top_k=top_k)
            matches = result.get("results", [])
            if not matches:
                st.info("No results. Upload resumes and configure Pinecone + OpenAI to enable search.")
            for i, match in enumerate(matches, start=1):
                metadata = match.get("metadata", {})
                st.markdown(f"**Result {i}** (score: {match.get('score', 'n/a')})")
                st.write(metadata.get("text", ""))
                st.divider()
        except Exception as exc:
            st.error(f"Search failed: {exc}")

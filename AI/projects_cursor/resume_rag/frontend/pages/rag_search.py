import streamlit as st

from services.rag_api import RagApi

st.title("RAG Search")

query = st.text_input("Search resumes")
top_k = st.slider("Results", min_value=1, max_value=20, value=5)

col1, col2 = st.columns(2)

with col1:
    search_clicked = st.button("Search", type="primary")

with col2:
    reindex_clicked = st.button("Re-index all resumes")

if reindex_clicked:
    with st.spinner("Indexing resumes into Pinecone..."):
        try:
            result = RagApi.reindex()
            st.success(f"Indexed {result.get('indexed_documents', 0)} document(s)")
            st.json(result)
        except Exception as exc:
            st.error(f"Re-index failed: {exc}")

if search_clicked:
    if not query:
        st.error("Enter a search query.")
    else:
        with st.spinner("Searching..."):
            try:
                result = RagApi.search(query, top_k=top_k)
                matches = result.get("results", [])
                if not matches:
                    st.info(
                        "No results found. Upload a resume, then click **Re-index all resumes**."
                    )
                for i, match in enumerate(matches, start=1):
                    metadata = match.get("metadata", {})
                    score = match.get("score")
                    score_label = f"{score:.3f}" if isinstance(score, (int, float)) else "n/a"
                    st.markdown(f"**Result {i}** (score: {score_label})")
                    st.write(metadata.get("text", ""))
                    st.caption(f"Document: {metadata.get('document_id', 'n/a')}")
                    st.divider()
            except Exception as exc:
                st.error(f"Search failed: {exc}")

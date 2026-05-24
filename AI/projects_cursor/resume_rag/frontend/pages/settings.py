import streamlit as st

from services.api import ApiClient

st.title("Settings & Connections")

st.subheader("Connection Status")

if st.button("Refresh status", type="primary"):
    st.session_state.pop("connections", None)

try:
    data = st.session_state.get("connections") or ApiClient.get("/connections")
    st.session_state["connections"] = data

    overall = data.get("status", "unknown")
    if overall == "ok":
        st.success(f"Overall: {overall}")
    elif overall == "degraded":
        st.warning(f"Overall: {overall}")
    else:
        st.info(f"Overall: {overall}")

    for conn in data.get("connections", []):
        status = conn.get("status", "unknown")
        icon = {"ok": "✅", "error": "❌", "degraded": "⚠️", "disabled": "⬜"}.get(status, "❓")
        with st.expander(f"{icon} {conn['name']} — {status}", expanded=status != "ok"):
            st.write(conn.get("message", ""))
            st.json(conn.get("details", {}))

except Exception as exc:
    st.error(f"Could not load connection status: {exc}")
    st.caption("Start the API with `make run` and ensure http://localhost:8000 is reachable.")

st.divider()
st.subheader("Environment keys")
st.caption("Set these in AI/.env and restart the app.")

st.markdown(
    """
| Service | Env vars |
|---------|----------|
| Database | `DB_PROVIDER`, Snowflake/MySQL vars |
| LLM | `GROQ_API_KEY`, `GROQ_MODEL` |
| RAG embeddings | `OPENAI_API_KEY` |
| Pinecone | `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, `PINECONE_NAMESPACE` |
| Redis queue | `USE_REDIS_QUEUE`, `REDIS_URL` |
| Langfuse | `LANGFUSE_PUBLIC_KEY`, `LANGFUSE_SECRET_KEY` |
"""
)

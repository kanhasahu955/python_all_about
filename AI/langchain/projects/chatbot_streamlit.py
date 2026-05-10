import sys
from pathlib import Path

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# AI/langchain/projects/this_file.py → repo root package is AI/
_AI_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_AI_ROOT) not in sys.path:
    sys.path.insert(0, str(_AI_ROOT))

from config.environment import get_settings

settings = get_settings()
settings.export_to_os_environ()

# ____________________________________

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite")

st.title("🤖 AskBuddy – AI QnA Bot")
st.markdown("My QnA Bot with LangChain and Google Gemini !")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

query = st.chat_input("Ask anything ?")

if query:
    st.session_state.messages.append({"role":"user", "content":query})
    st.chat_message("user").markdown(query)
    res = llm.invoke(query)
    st.chat_message("ai").markdown(res.content)
    st.session_state.messages.append({"role":"ai", "content":res.content})

import streamlit as st
import pandas as pd

st.title(
    "Agent Runs"
)

df = pd.DataFrame(
    [
        {
            "agent": "Parser",
            "status": "Success"
        },
        {
            "agent": "Skill Extractor",
            "status": "Success"
        },
        {
            "agent": "JD Matcher",
            "status": "Success"
        }
    ]
)

st.dataframe(df)
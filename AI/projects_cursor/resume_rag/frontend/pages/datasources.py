import streamlit as st

st.title(
    "Snowflake Datasources"
)

provider = st.selectbox(
    "Provider",
    [
        "snowflake",
        "mysql",
        "postgres",
        "sqlserver",
        "databricks",
        "bigquery"
    ]
)

host = st.text_input(
    "Host"
)

database = st.text_input(
    "Database"
)

schema = st.text_input(
    "Schema"
)

if st.button(
    "Test Connection"
):

    st.success(
        "Connection Successful"
    )
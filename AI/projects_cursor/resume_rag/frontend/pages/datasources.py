import streamlit as st

from services.datasource_api import DatasourceApi

st.title("Datasources")

col1, col2 = st.columns(2)
with col1:
    if st.button("Test app database (.env)", type="primary"):
        with st.spinner("Testing configured database…"):
            try:
                result = DatasourceApi.test_app_database()
                if result.get("success"):
                    st.success(f"{result.get('message')} ({result.get('provider')})")
                else:
                    st.error(result.get("message", "Connection failed"))
            except Exception as exc:
                st.error(f"Test failed: {exc}")

with col2:
    if st.button("Refresh saved datasources"):
        st.session_state.pop("datasources", None)

st.divider()
st.subheader("Test a connection")

provider = st.selectbox(
    "Provider",
    ["mysql", "postgres", "snowflake", "databricks"],
)

host = st.text_input("Host / account", placeholder="localhost or TEUFSHH-LR20472")
port = st.number_input("Port (MySQL/Postgres)", min_value=1, max_value=65535, value=3306)
username = st.text_input("Username")
password = st.text_input("Password", type="password")
database = st.text_input("Database")
schema = st.text_input("Schema", value="PUBLIC")
warehouse = st.text_input("Warehouse (Snowflake)", value="")
role = st.text_input("Role (Snowflake)", value="")
http_path = st.text_input("HTTP path (Databricks)", value="")
token = st.text_input("Token (Databricks)", type="password")

if st.button("Test Connection"):
    payload = {
        "provider": provider,
        "host": host or None,
        "port": int(port) if provider in {"mysql", "postgres"} else None,
        "username": username or None,
        "password": password or None,
        "database_name": database or None,
        "schema_name": schema or None,
        "warehouse": warehouse or None,
        "role": role or None,
        "http_path": http_path or None,
        "token": token or None,
    }
    with st.spinner("Connecting…"):
        try:
            result = DatasourceApi.test_connection(payload)
            if result.get("success"):
                st.success(result.get("message", "Connected"))
            else:
                st.error(result.get("message", "Connection failed"))
        except Exception as exc:
            st.error(f"Test failed: {exc}")

st.divider()
st.subheader("Saved datasources")

try:
    sources = st.session_state.get("datasources") or DatasourceApi.list_datasources()
    st.session_state["datasources"] = sources
    if sources:
        st.dataframe(sources, width="stretch")
    else:
        st.info("No saved datasources yet.")
except Exception as exc:
    st.error(f"Could not load datasources: {exc}")

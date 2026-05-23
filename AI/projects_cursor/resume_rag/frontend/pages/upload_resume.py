import streamlit as st

from services.resume_api import ResumeApi

st.title("Upload Resume")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
jd = st.text_area("Job Description (optional)")

if st.button("Analyze Resume"):
    if not uploaded_file:
        st.error("Please upload a PDF resume.")
    else:
        with st.spinner("Uploading and analyzing..."):
            try:
                result = ResumeApi.upload_resume(uploaded_file, jd)
                st.success("Upload complete!")
                st.json(result)
                if result.get("document_id"):
                    st.info(f"Document ID: `{result['document_id']}`")
            except Exception as exc:
                st.error(f"Upload failed: {exc}")

import streamlit as st

from services.resume_api import ResumeApi

st.title(
    "Upload Resume"
)

uploaded_file = st.file_uploader(
    "Upload Resume",
    type=[
        "pdf",
        "docx"
    ]
)

jd = st.text_area(
    "Job Description"
)

if st.button(
    "Analyze Resume"
):

    if uploaded_file:

        result = ResumeApi.upload_resume(
            uploaded_file,
            jd
        )

        st.success(
            "Uploaded Successfully"
        )

        st.json(result)
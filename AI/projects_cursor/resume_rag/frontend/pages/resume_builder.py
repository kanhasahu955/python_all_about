import streamlit as st

st.title(
    "Resume Builder"
)

resume = st.text_area(
    "Resume"
)

target_role = st.text_input(
    "Target Role"
)

if st.button(
    "Generate Resume"
):

    st.markdown(
        """
        # Optimized Resume
        """
    )
import streamlit as st
from core.models import generate_summary

def render_summary_view():
    st.subheader("📝 Study Guide & Summarizer")
    st.caption("Paste long articles or copy textbook notes to generate high-yield study templates.")

    text_input = st.text_area("Paste your study content here:", height=250, placeholder="Enter lecture text...")
    
    if st.button("Generate Study Guide", type="primary"):
        if text_input.strip():
            with st.spinner("Synthesizing key insights..."):
                summary_result = generate_summary(text_input)
                st.markdown("---")
                st.markdown(summary_result)
        else:
            st.warning("Please provide context text before generating.")
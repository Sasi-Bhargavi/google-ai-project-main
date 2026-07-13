import streamlit as st
from ui.chat_interface import render_chat_view
from ui.summary_interface import render_summary_view
from ui.quiz_interface import render_quiz_view

# Configure browser layout window parameters
st.set_page_config(
    page_title="EduGenie AI",
    page_icon="🎓",
    layout="centered"
)

# Global Application Dashboard Header
st.title("🎓 EduGenie Learning Assistant")
st.write("Your personal AI-powered workspace for accelerated learning.")
st.markdown("---")

# Navigation Selector Panel
st.sidebar.title("📚 Navigation")
st.sidebar.caption("Switch between active tools")
app_mode = st.sidebar.radio(
    "Go to:",
    ["Q&A Assistant", "Notes Summarizer", "Quiz Generator"]
)

# Route execution threads dynamically
if app_mode == "Q&A Assistant":
    render_chat_view()
elif app_mode == "Notes Summarizer":
    render_summary_view()
elif app_mode == "Quiz Generator":
    render_quiz_view()
import streamlit as st
import google.generativeai as genai

def get_gemini_client():
    """Initializes and authenticates the Gemini API client using Streamlit secrets."""
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_ACTUAL_GOOGLE_GEMINI_API_KEY_HERE":
        st.error("Missing Gemini API Key. Please add it to your .streamlit/secrets.toml file.")
        st.stop()
    
    genai.configure(api_key=api_key)
    return genai
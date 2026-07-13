import streamlit as st
from core.models import get_chat_response

def render_chat_view():
    st.subheader("🤖 Ask EduGenie")
    st.caption("Clear, interactive answers for any subject or concept.")

    # Initialize permanent persistent chat logs
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Print historical message logs
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user submission
    if prompt := st.chat_input("What concept can I help you break down today?"):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response_text = get_chat_response(st.session_state.chat_history)
                st.markdown(response_text)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
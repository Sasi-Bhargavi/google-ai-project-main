import streamlit as st
from core.models import generate_quiz

def render_quiz_view():
    st.subheader("🧠 Concept Check Quizzes")
    st.caption("Test your knowledge. Enter a subject below to build an on-demand multiple-choice exam.")

    topic = st.text_input("Quiz Topic:", placeholder="e.g., Photosynthesis, Newtonian Physics, Ancient Rome")
    
    if st.button("Generate Quiz", type="primary"):
        if topic.strip():
            with st.spinner("Formulating items..."):
                # Reset quiz state for a new topic choice
                st.session_state.quiz_data = generate_quiz(topic)
                st.session_state.quiz_submitted = False
        else:
            st.warning("Please enter a topic name.")

    # Render data if active array exists within current instance
    if "quiz_data" in st.session_state:
        st.markdown("---")
        user_answers = {}
        
        # Build individual questions
        for idx, q in enumerate(st.session_state.quiz_data):
            st.markdown(f"**Q{idx+1}: {q['question']}**")
            user_answers[idx] = st.radio(
                "Select one option:", 
                options=q['options'], 
                key=f"q_{idx}"
            )
            st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Submit Assessment"):
            st.session_state.quiz_submitted = True

        if st.get("quiz_submitted"):
            score = 0
            for idx, q in enumerate(st.session_state.quiz_data):
                if user_answers[idx] == q['correct_answer']:
                    score += 1
                    st.success(f"Question {idx+1}: Correct!")
                else:
                    st.error(f"Question {idx+1}: Incorrect. Correct answer was: {q['correct_answer']}")
            
            st.metric("Final Score", f"{score} / {len(st.session_state.quiz_data)}")
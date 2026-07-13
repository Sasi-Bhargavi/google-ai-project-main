import json
from core.client import get_gemini_client
from core.prompt_templates import QA_SYSTEM_PROMPT, SUMMARIZATION_PROMPT, QUIZ_PROMPT

def get_chat_response(messages):
    """Handles conversational multi-turn Q&A."""
    ai = get_gemini_client()
    # Using 1.5 Flash for rapid text responses
    model = ai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=QA_SYSTEM_PROMPT
    )
    
    # Format the chat history for the official SDK
    formatted_history = []
    for msg in messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        formatted_history.append({"role": role, "parts": [msg["content"]]})
        
    chat = model.start_chat(history=formatted_history)
    response = chat.send_message(messages[-1]["content"])
    return response.text

def generate_summary(text_content):
    """Processes long text strings into key summaries."""
    ai = get_gemini_client()
    model = ai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SUMMARIZATION_PROMPT
    )
    response = model.generate_content(text_content)
    return response.text

def generate_quiz(topic_text):
    """Generates structured multiple-choice questions via JSON enforcement."""
    ai = get_gemini_client()
    model = ai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=QUIZ_PROMPT
    )
    
    response = model.generate_content(f"Generate a quiz about: {topic_text}")
    try:
        # Clean response text of accidental markdown wrapping formatting if present
        clean_text = response.text.strip().strip("```json").strip("```").strip()
        return json.loads(clean_text)
    except Exception as e:
        return [{"question": "Failed to parse quiz schema.", "options": ["Error"], "correct_answer": "Error"}]
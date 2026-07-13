import os
import google.generativeai as genai
from fastapi import HTTPException

# Configure API Key securely via environment variable
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=API_KEY)

def ask_gemini_pro(prompt: str, system_instruction: str = None) -> str:
    """Queries Gemini 1.5 Pro for intensive reasoning or document parsing tasks."""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=system_instruction
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")
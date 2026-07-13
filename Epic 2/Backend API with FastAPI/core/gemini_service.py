import os
import google.generativeai as genai
from fastapi import HTTPException

# Fetch and verify the API key from the environment map
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
    raise RuntimeError("CRITICAL ERROR: Valid GEMINI_API_KEY is not defined in the environment layout.")

genai.configure(api_key=API_KEY)

def ask_gemini_pro(prompt: str, system_instruction: str = None) -> str:
    """
    Connects to cloud-hosted Gemini 1.5 Pro to process high-level multi-turn reasoning 
    or text document synthesis tasks.
    """
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            system_instruction=system_instruction
        )
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Cloud-Based Gemini 1.5 Pro Platform Core Failure: {str(e)}"
        )
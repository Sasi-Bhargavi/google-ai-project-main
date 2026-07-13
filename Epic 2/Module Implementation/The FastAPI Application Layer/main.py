from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import json

from core.gemini_service import ask_gemini_pro
from core.lamini_service import query_lamini

app = FastAPI(
    title="EduGenie AI Core Backend",
    description="Hybrid API gateway managing cloud LLMs and localized compute engines."
)

# --- REQUEST/RESPONSE SCHEMAS ---
class ChatMessage(BaseModel):
    role: str  # 'user' or 'assistant'
    content: str

class ChatPayload(BaseModel):
    message: str
    history: List[ChatMessage] = []

class QuizRequest(BaseModel):
    topic: str
    num_questions: Optional[int] = 3

class RecommendationRequest(BaseModel):
    score: int
    total_questions: int
    topic: str

# --- ENDPOINTS ---

@app.post("/api/v1/chat", summary="Complex Concept Explanations (Gemini 1.5 Pro)")
async def chat_explanation(payload: ChatPayload):
    system_instruction = (
        "You are EduGenie, an elite academic private tutor. Explain concepts using "
        "vivid analogies, structural bolding, and highly intuitive breakdowns."
    )
    
    # Format structural multi-turn context arrays for Gemini Pro processing
    full_context = ""
    for msg in payload.history:
        full_context += f"{msg.role.capitalize()}: {msg.content}\n"
    full_context += f"User: {payload.message}\nAssistant:"

    response_text = ask_gemini_pro(full_context, system_instruction=system_instruction)
    return {"response": response_text}


@app.post("/api/v1/summarize", summary="High-Yield Document Synthesis (Gemini 1.5 Pro)")
async def summarize_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="Currently supporting raw .txt or .md assets.")
        
    contents = await file.read()
    document_text = contents.decode("utf-8")
    
    prompt = (
        f"Synthesize the following material into a rigorous student study guide. "
        f"Include a high-level summary, a key definitions checklist, and study takeaways:\n\n{document_text}"
    )
    
    summary_output = ask_gemini_pro(prompt, system_instruction="You are an expert academic editor.")
    return {"summary": summary_output}


@app.post("/api/v1/quiz", summary="Localized Quiz Generation (LaMini-Flan-T5)")
async def generate_quiz_local(request: QuizRequest):
    # Constructing strict task prompts for local small-scale execution
    prompt = (
        f"Generate a quiz with {request.num_questions} questions about: {request.topic}. "
        f"Format explicitly as: Q: [Question] A) [Opt 1] B) [Opt 2] Correct: [Answer]"
    )
    
    raw_output = query_lamini(prompt, max_length=512)
    return {"quiz_raw": raw_output}


@app.post("/api/v1/recommendations", summary="Immediate Remediation Paths (LaMini-Flan-T5)")
async def fetch_recommendations(req: RecommendationRequest):
    percentage = (req.score / req.total_questions) * 100
    
    prompt = (
        f"A student scored {req.score}/{req.total_questions} ({percentage:.1f}%) on a quiz about '{req.topic}'. "
        f"Provide exactly two short bulleted recommendations for what they should study next based on this outcome."
    )
    
    recommendation_output = query_lamini(prompt, max_length=256)
    return {"recommendations": recommendation_output}
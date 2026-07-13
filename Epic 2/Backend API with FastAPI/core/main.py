import os
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Step 1: Pre-load the workspace keys from .env layout before initializing services
load_dotenv()

from core.gemini_service import ask_gemini_pro
from core.lamini_service import query_lamini

# Initialize FastAPI App Engine
app = FastAPI(
    title="💡 EduGenie AI Backend Engine",
    description="Asynchronous Hybrid Backend Gateway managing cloud LLMs and localized compute engines.",
    version="2.0.0"
)

# Configure Cross-Origin Resource Sharing (CORS) rules for local frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PYDANTIC SCHEMAS ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class QuizRequest(BaseModel):
    topic: str
    num_questions: Optional[int] = Field(default=3, ge=1, le=10)

class RemediationRequest(BaseModel):
    score: int
    total_questions: int
    topic: str

# --- APIS ---
@app.get("/health", tags=["System Monitoring"])
async def health():
    return {"status": "online", "message": "EduGenie Core Router is functioning properly."}

@app.post("/api/v2/chat", tags=["Academic Core"])
async def chat_explanation(payload: ChatRequest):
    system_instruction = (
        "You are EduGenie, an expert conversational academic tutor. Explain rules and complex ideas "
        "step-by-step using structural bolding, formatting, and helpful real-world analogies."
    )
    formatted_context = ""
    for msg in payload.history:
        formatted_context += f"{msg.role.capitalize()}: {msg.content}\n"
    formatted_context += f"User: {payload.message}\nAssistant:"

    response_text = ask_gemini_pro(formatted_context, system_instruction=system_instruction)
    return {"response": response_text}

@app.post("/api/v2/summarize", tags=["Academic Core"])
async def summarize_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="Unsupported format. Raw .txt or .md assets only.")
        
    contents = await file.read()
    document_text = contents.decode("utf-8")
    
    prompt = f"Deconstruct and synthesize this reference material into a master study outline:\n\n{document_text}"
    summary_output = ask_gemini_pro(prompt, system_instruction="You are an expert academic editor.")
    return {"summary": summary_output}

@app.post("/api/v2/quiz", tags=["Local Analytics"])
async def generate_quiz_local(request: QuizRequest):
    prompt = (
        f"Generate a brief quiz containing exactly {request.num_questions} questions about: {request.topic}. "
        f"Format explicitly as: Q: [Question] A) [Option 1] B) [Option 2] Correct: [Answer]"
    )
    raw_quiz_data = query_lamini(prompt, max_length=512)
    return {"quiz_raw": raw_quiz_data}

@app.post("/api/v2/recommendations", tags=["Local Analytics"])
async def fetch_recommendations(req: RemediationRequest):
    percentage = (req.score / req.total_questions) * 100
    prompt = (
        f"A student scored {req.score}/{req.total_questions} ({percentage:.1f}%) on a quiz about '{req.topic}'. "
        f"Provide two concise bullet points recommending what specific core concepts they should review next."
    )
    recommendation_output = query_lamini(prompt, max_length=256)
    return {"recommendations": recommendation_output}
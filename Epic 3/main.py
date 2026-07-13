import os
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

from core.gemini_service import ask_gemini_pro
from core.lamini_service import query_lamini

app = FastAPI(title="🎓 EduGenie Web Platform", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MOUNT STATIC FILES & JINJA TEMPLATES ---
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# --- DATA SCHEMAS ---
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: List[ChatMessage] = []

class QuizRequest(BaseModel):
    topic: str
    num_questions: Optional[int] = 3

class RemediationRequest(BaseModel):
    score: int
    total_questions: int
    topic: str

# --- WEB PAGE CONTROLLER ROUTES ---

@app.get("/", tags=["Web Pages"])
async def render_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request, "active_page": "chat"})

@app.get("/summarizer", tags=["Web Pages"])
async def render_summary_page(request: Request):
    return templates.TemplateResponse("summary.html", {"request": request, "active_page": "summary"})

@app.get("/quiz-engine", tags=["Web Pages"])
async def render_quiz_page(request: Request):
    return templates.TemplateResponse("quiz.html", {"request": request, "active_page": "quiz"})


@app.post("/api/v2/chat")
async def chat_explanation(payload: ChatRequest):
    system_instruction = "You are EduGenie, an expert academic tutor. Explain simply using structured bolding and analogies."
    formatted_context = "".join([f"{msg.role.capitalize()}: {msg.content}\n" for msg in payload.history])
    formatted_context += f"User: {payload.message}\nAssistant:"
    
    response_text = ask_gemini_pro(formatted_context, system_instruction=system_instruction)
    return {"response": response_text}

@app.post("/api/v2/summarize")
async def summarize_document(file: UploadFile = File(...)):
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(status_code=400, detail="Unsupported format. Raw .txt or .md assets only.")
    contents = await file.read()
    document_text = contents.decode("utf-8")
    
    prompt = f"Deconstruct and synthesize this reference material into an elite structured master study outline:\n\n{document_text}"
    summary_output = ask_gemini_pro(prompt, system_instruction="You are an expert academic editor.")
    return {"summary": summary_output}

@app.post("/api/v2/quiz")
async def generate_quiz_local(request: QuizRequest):
    prompt = f"Generate a short quiz with exactly {request.num_questions} questions about: {request.topic}. Format as: Q: [Question] A) [Opt 1] B) [Opt 2] Correct: [Answer]"
    raw_quiz_data = query_lamini(prompt, max_length=512)
    return {"quiz_raw": raw_quiz_data}

@app.post("/api/v2/recommendations")
async def fetch_recommendations(req: RemediationRequest):
    percentage = (req.score / req.total_questions) * 100
    prompt = f"A student scored {req.score}/{req.total_questions} ({percentage:.1f}%) on a quiz about '{req.topic}'. Give two short tips on what to study next."
    recommendation_output = query_lamini(prompt, max_length=256)
    return {"recommendations": recommendation_output}
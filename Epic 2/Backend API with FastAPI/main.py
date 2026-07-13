import os
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Local dependency imports from your core service files
from core.gemini_service import ask_gemini_pro
from core.lamini_service import query_lamini

# Initialize FastAPI App Instance
app = FastAPI(
    title="💡 EduGenie AI Gateway Engine",
    description="Asynchronous Hybrid Backend processing API nodes for modular learning structures.",
    version="2.0.0"
)

# Configure Cross-Origin Resource Sharing (CORS) 
# Allows your Streamlit or static frontend views to securely query this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with specific origins like ["http://localhost:8501"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PYDANTIC VALIDATION SCHEMAS ---

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the speaker: 'user' or 'assistant'")
    content: str = Field(..., description="The raw textual statement")

class ChatRequest(BaseModel):
    message: str = Field(..., description="The latest query sent by the student")
    history: List[ChatMessage] = Field(default=[], description="Thread records for contextual memory tracking")

class QuizRequest(BaseModel):
    topic: str = Field(..., min_length=2, max_length=100, example="Quantum Computing basics")
    num_questions: Optional[int] = Field(default=3, ge=1, le=10)

class RemediationRequest(BaseModel):
    score: int = Field(..., ge=0)
    total_questions: int = Field(..., ge=1)
    topic: str = Field(..., min_length=2)

# --- SYSTEM MONITORING ENDPOINTS ---

@app.get("/health", status_code=status.HTTP_200_OK, tags=["System Health"])
async def health_check():
    """System heartbeat verification loop."""
    return {"status": "healthy", "environment": "active"}

# --- CORE EDUCATIONAL ROUTE MODULES ---

@app.post("/api/v2/chat", tags=["Academic Core"], status_code=status.HTTP_200_OK)
async def chat_explanation(payload: ChatRequest):
    """
    Invokes Gemini 1.5 Pro to process high-level reasoning and analytical breakdowns.
    """
    system_instruction = (
        "You are EduGenie, an advanced academic tutor. Explain ideas step-by-step "
        "using bold headers, simple analogies, and a clean structured layout."
    )
    
    # Format structural historical conversational maps for token string extraction
    formatted_context = ""
    for msg in payload.history:
        formatted_context += f"{msg.role.capitalize()}: {msg.content}\n"
    formatted_context += f"User: {payload.message}\nAssistant:"

    response_text = ask_gemini_pro(formatted_context, system_instruction=system_instruction)
    return {"response": response_text}


@app.post("/api/v2/summarize", tags=["Academic Core"], status_code=status.HTTP_200_OK)
async def summarize_document(file: UploadFile = File(...)):
    """
    Ingests flat lecture text or markdown documents and maps them through 
    Gemini 1.5 Pro's massive token context window for summarization.
    """
    # Enforce clear asset constraints
    if not file.filename.endswith(('.txt', '.md')):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Unsupported format. Please upload text (.txt) or markdown (.md) documents."
        )
        
    try:
        contents = await file.read()
        document_text = contents.decode("utf-8")
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Failed to decode file streams. Ensure asset uses UTF-8 parsing standard."
        )
    
    prompt = (
        f"Analyze the following textbook/lecture materials and compress it into an expert study guide. "
        f"Format with a high-level summary, key term definitions, and actionable takeaways:\n\n{document_text}"
    )
    
    summary_output = ask_gemini_pro(prompt, system_instruction="You are an expert academic editor.")
    return {"summary": summary_output}


@app.post("/api/v2/quiz", tags=["Local Analytics"], status_code=status.HTTP_200_OK)
async def generate_quiz_local(request: QuizRequest):
    """
    Queries your local, cost-free LaMini-Flan-T5 model instance to generate 
    deterministic conceptual question items.
    """
    prompt = (
        f"Generate a quiz containing exactly {request.num_questions} questions about: {request.topic}. "
        f"Format style: Q: [Question] A) [Opt] B) [Opt] C) [Opt] Correct: [Answer]"
    )
    
    raw_quiz_data = query_lamini(prompt, max_length=512)
    return {"quiz_raw": raw_quiz_data}


@app.post("/api/v2/recommendations", tags=["Local Analytics"], status_code=status.HTTP_200_OK)
async def fetch_recommendations(req: RemediationRequest):
    """
    Leverages localized LaMini loops to process score percentages and output 
    immediate, automated study remediation blueprints.
    """
    if req.score > req.total_questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Score cannot exceed total question matrix thresholds."
        )
        
    percentage = (req.score / req.total_questions) * 100
    
    prompt = (
        f"A student scored {req.score}/{req.total_questions} ({percentage:.1f}%) on a quiz about '{req.topic}'. "
        f"Provide two concise bullet points recommending what specific core concepts they should review next."
    )
    
    recommendation_output = query_lamini(prompt, max_length=256)
    return {"recommendations": recommendation_output}
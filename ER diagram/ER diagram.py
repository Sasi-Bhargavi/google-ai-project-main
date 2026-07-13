from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

USER ENTITY SCHEMAS
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserSchema(UserBase):
    user_id: int
    created_at: datetime
    class Config: from_attributes = True

2. USER QUERY ENTITY SCHEMAS
class UserQueryBase(BaseModel):
    query_type: str  # QnA, Explanation, Quiz, Summary, Recommendation
    query_text: str

class UserQueryCreate(UserQueryBase):
    user_id: int

class UserQuerySchema(UserQueryBase):
    query_id: int
    user_id: int
    created_at: datetime
    class Config: from_attributes = True

3. AI RESPONSE ENTITY SCHEMAS (1-to-1 with UserQuery)
class AIResponseSchema(BaseModel):
    response_id: int
    query_id: int
    response_text: str
    model_used: str  # Gemini 1.5 Pro vs LaMini-Flan-T5
    created_at: datetime
    class Config: from_attributes = True

4. QUIZ ENTITY SCHEMAS (1-to-Many with UserQuery)
class QuizSchema(BaseModel):
    quiz_id: int
    query_id: int
    question_text: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str
    created_at: datetime
    class Config: from_attributes = True

5. SUMMARY ENTITY SCHEMAS (1-to-Many with UserQuery)
class SummarySchema(BaseModel):
    summary_id: int
    query_id: int
    summary_text: str
    created_at: datetime
    class Config: from_attributes = True

6. LEARNING PATH ENTITY SCHEMAS (1-to-Many with UserQuery)
class LearningPathSchema(BaseModel):
    path_id: int
    query_id: int
    topic: str
    difficulty_level: str
    recommended_resources: str
    created_at: datetime
    class Config: from_attributes = True
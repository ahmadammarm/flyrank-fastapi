from pydantic import BaseModel
from typing import List, Optional

class DocumentCreate(BaseModel):
    title: str
    content: str

class DocumentResponse(BaseModel):
    id: int
    title: str
    created_at: str

class ChatRequest(BaseModel):
    session_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    session_id: int
    reply: str

class FeedbackRequest(BaseModel):
    message_id: int
    is_positive: bool
    comments: Optional[str] = None

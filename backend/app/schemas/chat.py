from pydantic import BaseModel
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str  # user, assistant
    content: str

class ChatRequest(BaseModel):
    workspace_id: str
    history: List[ChatMessage]
    
class Citation(BaseModel):
    path: str
    title: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[Citation]
    insufficient_coverage: bool = False

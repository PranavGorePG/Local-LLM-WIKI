from pydantic import BaseModel
from typing import List

class DocumentResponse(BaseModel):
    filename: str
    category: str  # pdf, txt, md
    size_bytes: int

class DocumentListResponse(BaseModel):
    documents: List[DocumentResponse]

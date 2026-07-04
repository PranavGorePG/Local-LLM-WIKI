from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Literal
from app.services.wiki_integrity_service import IntegrityReport

class IngestRequest(BaseModel):
    workspace_id: str
    document_names: Optional[List[str]] = None  # None means all documents

class IngestResult(BaseModel):
    pages_created: int
    pages_updated: int
    summary: str

class WikiPageMetadata(BaseModel):
    title: str
    type: Literal["source", "concept", "entity", "topic", "person"]
    source_documents: List[str] = Field(default_factory=list)
    related_pages: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    confidence: Optional[str] = None
    updated: Optional[str] = None
    affiliation: Optional[str] = None

class WikiPageUpdate(BaseModel):
    metadata: WikiPageMetadata
    content: str
    slug: str

class WikiPageResponse(BaseModel):
    path: str
    metadata: dict
    content: str

class LintIssue(BaseModel):
    severity: str  # error, warning, suggestion
    path: str
    message: str

class LintResult(BaseModel):
    issues: List[LintIssue]

class RepairResult(BaseModel):
    pages_repaired: int
    pages_deleted: int
    summary: str
    integrity: Optional[IntegrityReport] = None

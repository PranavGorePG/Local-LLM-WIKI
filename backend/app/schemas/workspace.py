from pydantic import BaseModel
from typing import List, Optional

class WorkspaceCreate(BaseModel):
    name: str

class WorkspaceResponse(BaseModel):
    workspace_id: str
    name: str
    path: str

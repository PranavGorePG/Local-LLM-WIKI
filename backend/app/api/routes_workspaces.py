from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.workspace import WorkspaceCreate, WorkspaceResponse
from app.services.workspace_service import WorkspaceService
from app.api.deps import get_workspace_service

router = APIRouter()

@router.get("", response_model=List[WorkspaceResponse])
def get_workspaces(service: WorkspaceService = Depends(get_workspace_service)):
    return service.list_workspaces()

@router.post("", response_model=WorkspaceResponse)
def create_workspace(data: WorkspaceCreate, service: WorkspaceService = Depends(get_workspace_service)):
    try:
        return service.create_workspace(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{workspace_id}", response_model=WorkspaceResponse)
def get_workspace(workspace_id: str, service: WorkspaceService = Depends(get_workspace_service)):
    try:
        path = service.resolve_workspace_path(workspace_id)
        return WorkspaceResponse(workspace_id=workspace_id, name=workspace_id, path=str(path))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Workspace not found")

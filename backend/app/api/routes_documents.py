from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from typing import List
from app.schemas.document import DocumentResponse, DocumentListResponse
from app.services.file_storage_service import FileStorageService
from app.api.deps import get_file_storage_service

router = APIRouter()

@router.get("", response_model=DocumentListResponse)
def list_documents(workspace_id: str, service: FileStorageService = Depends(get_file_storage_service)):
    try:
        docs = service.list_documents(workspace_id)
        return DocumentListResponse(documents=docs)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    workspace_id: str, 
    file: UploadFile = File(...), 
    service: FileStorageService = Depends(get_file_storage_service)
):
    try:
        return service.save_upload(workspace_id, file)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{document_name}")
def delete_document(
    workspace_id: str, 
    document_name: str, 
    service: FileStorageService = Depends(get_file_storage_service)
):
    try:
        service.delete_document(workspace_id, document_name)
        return {"status": "success"}
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Document not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

import os
import shutil
from pathlib import Path
from fastapi import UploadFile
from typing import List

from app.core.constants import RAW_DIR_NAME, ALLOWED_EXTENSIONS
from app.schemas.document import DocumentResponse
from app.services.workspace_service import WorkspaceService
from app.core.logger import get_logger

logger = get_logger(__name__)

class FileStorageService:
    def __init__(self, workspace_service: WorkspaceService):
        self.workspace_service = workspace_service

    def _get_raw_dir(self, workspace_id: str) -> Path:
        workspace_path = self.workspace_service.resolve_workspace_path(workspace_id)
        return workspace_path / RAW_DIR_NAME

    def _get_subfolder_for_extension(self, ext: str) -> str:
        ext = ext.lower()
        if ext == ".pdf":
            return "pdf"
        elif ext in [".txt", ".md"]:
            return ext[1:]
        return "txt"

    def list_documents(self, workspace_id: str) -> List[DocumentResponse]:
        raw_dir = self._get_raw_dir(workspace_id)
        docs = []
        for ext_folder in ["pdf", "txt", "md"]:
            folder_path = raw_dir / ext_folder
            if folder_path.exists():
                for file_path in folder_path.iterdir():
                    if file_path.is_file():
                        docs.append(DocumentResponse(
                            filename=file_path.name,
                            category=ext_folder,
                            size_bytes=file_path.stat().st_size
                        ))
        return docs

    def save_upload(self, workspace_id: str, file: UploadFile) -> DocumentResponse:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Extension {ext} not allowed. Allowed: {ALLOWED_EXTENSIONS}")
            
        raw_dir = self._get_raw_dir(workspace_id)
        subfolder = self._get_subfolder_for_extension(ext)
        dest_path = raw_dir / subfolder / file.filename
        
        # Prevent traversal
        if not str(dest_path.resolve()).startswith(str(raw_dir.resolve())):
            raise ValueError("Invalid filename")
            
        with dest_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return DocumentResponse(
            filename=file.filename,
            category=subfolder,
            size_bytes=dest_path.stat().st_size
        )

    def delete_document(self, workspace_id: str, filename: str):
        raw_dir = self._get_raw_dir(workspace_id)
        for ext_folder in ["pdf", "txt", "md"]:
            file_path = raw_dir / ext_folder / filename
            if file_path.exists():
                # Check traversal
                if not str(file_path.resolve()).startswith(str(raw_dir.resolve())):
                    raise ValueError("Invalid filename")
                file_path.unlink()
                return True
        raise FileNotFoundError(f"Document {filename} not found")
    
    def get_document_path(self, workspace_id: str, filename: str) -> Path:
        raw_dir = self._get_raw_dir(workspace_id)
        for ext_folder in ["pdf", "txt", "md"]:
            file_path = raw_dir / ext_folder / filename
            if file_path.exists():
                if not str(file_path.resolve()).startswith(str(raw_dir.resolve())):
                    raise ValueError("Invalid filename")
                return file_path
        raise FileNotFoundError(f"Document {filename} not found")

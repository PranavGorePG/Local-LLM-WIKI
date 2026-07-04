from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.wiki import IngestRequest, IngestResult, WikiPageResponse, LintResult, RepairResult
from app.services.wiki_compiler_service import WikiCompilerService
from app.services.wiki_lint_service import WikiLintService
from app.services.wiki_repair_service import WikiRepairService
from app.services.wiki_integrity_service import IntegrityReport, WikiIntegrityService
from app.services.wiki_repository import WikiRepository
from app.api.deps import get_wiki_compiler_service, get_wiki_lint_service, get_wiki_repository, get_wiki_repair_service, get_wiki_integrity_service

router = APIRouter()

@router.post("/ingest", response_model=IngestResult)
def ingest_documents(
    request: IngestRequest, 
    service: WikiCompilerService = Depends(get_wiki_compiler_service)
):
    try:
        return service.compile(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pages", response_model=List[str])
def list_wiki_pages(
    workspace_id: str, 
    repo: WikiRepository = Depends(get_wiki_repository)
):
    try:
        return repo.list_pages(workspace_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/page", response_model=WikiPageResponse)
def get_wiki_page(
    workspace_id: str, 
    path: str, 
    repo: WikiRepository = Depends(get_wiki_repository)
):
    try:
        metadata, content = repo.read_page(workspace_id, path)
        return WikiPageResponse(path=path, metadata=metadata, content=content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Page not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/lint", response_model=LintResult)
def lint_wiki(
    workspace_id: str, 
    service: WikiLintService = Depends(get_wiki_lint_service)
):
    try:
        return service.lint_wiki(workspace_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/repair", response_model=RepairResult)
def repair_wiki(
    workspace_id: str,
    service: WikiRepairService = Depends(get_wiki_repair_service)
):
    try:
        # Run lint first to get current issues
        lint_service = get_wiki_lint_service()
        lint_result = lint_service.lint_wiki(workspace_id)
        return service.repair_wiki(workspace_id, lint_result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/integrity", response_model=IntegrityReport)
def check_wiki_integrity(
    workspace_id: str,
    service: WikiIntegrityService = Depends(get_wiki_integrity_service)
):
    try:
        return service.run_integrity_check(workspace_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/integrity/repair", response_model=IntegrityReport)
def repair_wiki_integrity(
    workspace_id: str,
    service: WikiIntegrityService = Depends(get_wiki_integrity_service)
):
    try:
        return service.run_integrity_check(workspace_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

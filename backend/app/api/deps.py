from typing import Generator
from app.services.workspace_service import WorkspaceService
from app.services.file_storage_service import FileStorageService
from app.services.document_parser_service import DocumentParserService
from app.services.gemini_service import GeminiService
from app.services.wiki_repository import WikiRepository
from app.services.wiki_compiler_service import WikiCompilerService
from app.services.wiki_query_service import WikiQueryService
from app.services.wiki_lint_service import WikiLintService

# Instantiate services once (singleton pattern for stateless services)
workspace_service = WorkspaceService()
file_storage_service = FileStorageService(workspace_service)
document_parser_service = DocumentParserService()
gemini_service = GeminiService()
wiki_repository = WikiRepository(workspace_service)
wiki_compiler_service = WikiCompilerService(
    workspace_service, file_storage_service, document_parser_service, gemini_service, wiki_repository
)
wiki_query_service = WikiQueryService(gemini_service, wiki_repository)
wiki_lint_service = WikiLintService(wiki_repository)

def get_workspace_service() -> WorkspaceService:
    return workspace_service

def get_file_storage_service() -> FileStorageService:
    return file_storage_service

def get_wiki_compiler_service() -> WikiCompilerService:
    return wiki_compiler_service

def get_wiki_query_service() -> WikiQueryService:
    return wiki_query_service

def get_wiki_lint_service() -> WikiLintService:
    return wiki_lint_service

def get_wiki_repository() -> WikiRepository:
    return wiki_repository

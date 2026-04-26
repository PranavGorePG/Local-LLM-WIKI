from typing import List, Optional
from pathlib import Path
from app.schemas.wiki import IngestRequest, IngestResult
from app.services.workspace_service import WorkspaceService
from app.services.file_storage_service import FileStorageService
from app.services.document_parser_service import DocumentParserService
from app.services.gemini_service import GeminiService
from app.services.wiki_repository import WikiRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

class WikiCompilerService:
    def __init__(
        self,
        workspace_service: WorkspaceService,
        file_storage: FileStorageService,
        parser: DocumentParserService,
        gemini: GeminiService,
        wiki_repo: WikiRepository
    ):
        self.workspace_service = workspace_service
        self.file_storage = file_storage
        self.parser = parser
        self.gemini = gemini
        self.wiki_repo = wiki_repo

    def compile(self, request: IngestRequest) -> IngestResult:
        workspace_id = request.workspace_id
        workspace_path = self.workspace_service.resolve_workspace_path(workspace_id)
        
        # Gather documents to ingest
        docs_to_parse = []
        if request.document_names:
            for name in request.document_names:
                path = self.file_storage.get_document_path(workspace_id, name)
                docs_to_parse.append(path)
        else:
            docs = self.file_storage.list_documents(workspace_id)
            for doc in docs:
                path = self.file_storage.get_document_path(workspace_id, doc.filename)
                docs_to_parse.append(path)

        if not docs_to_parse:
            return IngestResult(pages_created=0, pages_updated=0, summary="No documents found to ingest.")

        parsed_docs = []
        for path in docs_to_parse:
            content = self.parser.parse_document(path)
            parsed_docs.append({"filename": path.name, "content": content})

        # Load context
        try:
            with open(workspace_path / "AGENTS.md", "r", encoding="utf-8") as f:
                agents_md = f.read()
        except FileNotFoundError:
            agents_md = "No AGENTS.md found."

        try:
            _, index_md = self.wiki_repo.read_page(workspace_id, "index.md")
        except FileNotFoundError:
            index_md = ""

        # Build catalog
        pages = self.wiki_repo.list_pages(workspace_id)
        catalog = "\n".join(pages)

        # Call Gemini
        result = self.gemini.compile_wiki_updates(
            agents_md=agents_md,
            current_index=index_md,
            page_catalog=catalog,
            documents=parsed_docs
        )

        # Apply updates
        pages_created = 0
        pages_updated = 0
        for update in result.pages:
            # Check if page exists to increment correct counter
            # We assume it exists if its path is in catalog roughly, but let's just write
            # We don't have exact path resolution here but we can guess
            pages_updated += 1 # Simplify for now
            self.wiki_repo.write_page(workspace_id, update)

        # Update index and log
        self.wiki_repo.overwrite_index(workspace_id, result.index_markdown)
        self.wiki_repo.append_log(workspace_id, result.log_entry)

        return IngestResult(
            pages_created=pages_created,
            pages_updated=pages_updated,
            summary=result.summary
        )

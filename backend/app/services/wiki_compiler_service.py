from typing import List, Optional
from pathlib import Path
from app.schemas.wiki import IngestRequest, IngestResult
from app.services.workspace_service import WorkspaceService
from app.services.file_storage_service import FileStorageService
from app.services.document_parser_service import DocumentParserService
from app.services.gemini_service import GeminiService
from app.services.wiki_repository import WikiRepository
from app.core.logger import get_logger
import re

logger = get_logger(__name__)

def _normalize_concept(name: str) -> str:
    """Normalize a concept name for fuzzy matching."""
    name = name.lower().strip()
    # Remove parenthetical abbreviations like (RNN), (NLP)
    name = re.sub(r'\(.*?\)', '', name)
    # Remove special characters
    name = re.sub(r'[^\w\s]', '', name)
    # Strip trailing 's' for basic plural normalization
    name = name.strip().rstrip('s')
    return name.strip()

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

        # Extract concepts from all documents
        concepts = self.gemini.extract_concepts(parsed_docs)
        
        # Load current index
        index_map = self.wiki_repo.parse_index(workspace_id)
        
        pages_created = 0
        pages_updated = 0
        
        # Load existing pages for concepts already in index
        existing_pages = {}
        
        # Build normalized index map for fuzzy matching
        normalized_index = {
            _normalize_concept(k): v 
            for k, v in index_map.items()
        }

        # When checking if concept exists, use normalized form
        for concept in concepts:
            name = concept['concept_name']
            normalized_name = _normalize_concept(name)
            
            if normalized_name in normalized_index:
                # concept exists — load existing page
                path = normalized_index[normalized_name]
                try:
                    existing_pages[name] = self.wiki_repo.read_page_raw(workspace_id, path)
                except FileNotFoundError:
                    existing_pages[name] = ""
            else:
                # concept is new
                existing_pages[name] = ""

        # Call 2 — batch compile all pages (1 Gemini call)
        page_updates = self.gemini.batch_compile_pages(
            concepts=concepts,
            existing_pages=existing_pages,
            documents=parsed_docs,
            agents_md=agents_md
        )

        # Write all pages to disk (no Gemini calls, pure file IO)
        for update in page_updates:
            self.wiki_repo.write_page(workspace_id, update)
            if update.slug in [v.split('/')[-1].replace('.md','') for v in index_map.values()]:
                pages_updated += 1
            else:
                pages_created += 1

        # Rebuild index
        self.wiki_repo.rebuild_index(workspace_id)
        
        # Append log
        log_entry = f"Ingested {len(parsed_docs)} documents, extracted {len(concepts)} concepts. Created {pages_created}, Updated {pages_updated}."
        self.wiki_repo.append_log(workspace_id, log_entry)

        return IngestResult(
            pages_created=pages_created,
            pages_updated=pages_updated,
            summary=log_entry
        )

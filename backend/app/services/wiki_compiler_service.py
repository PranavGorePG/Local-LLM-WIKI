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
        
        # Deduplication Pass
        type_priority = {
            "person": 5,
            "entity": 4,
            "concept": 3,
            "topic": 2,
            "source": 1
        }
        
        deduped = {}
        for concept in concepts:
            name = concept['concept_name']
            norm = _normalize_concept(name)
            if not norm:
                continue
                
            ctype = concept['concept_type']
            
            if norm not in deduped:
                deduped[norm] = concept
            else:
                existing = deduped[norm]
                ex_type = existing['concept_type']
                
                if type_priority.get(ctype, 0) > type_priority.get(ex_type, 0):
                    deduped[norm] = concept
                elif type_priority.get(ctype, 0) == type_priority.get(ex_type, 0):
                    if len(name) > len(existing['concept_name']):
                        deduped[norm] = concept
                        
        initial_count = len(concepts)
        concepts = list(deduped.values())
        final_count = len(concepts)
        if initial_count > final_count:
            logger.info(f"Removed {initial_count - final_count} duplicates during concept deduplication pass.")
        
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
        all_page_updates = self.gemini.batch_compile_pages(
            concepts=concepts,
            existing_pages=existing_pages,
            documents=parsed_docs,
            agents_md=agents_md
        )

        person_pages = []
        regular_pages = []
        for update in all_page_updates:
            if update.metadata.type == "person":
                person_pages.append(update)
            else:
                regular_pages.append(update)

        import re
        from pathlib import Path
        
        raw_authors = []
        for p in person_pages:
            paper_title = "Unknown Paper"
            if p.metadata.source_documents:
                stem = Path(p.metadata.source_documents[0]).stem
                
                found_title = None
                # Check if it's already in the index
                if stem in index_map:
                    rel_path = index_map[stem]
                    try:
                        meta, _ = self.wiki_repo.read_page(workspace_id, rel_path)
                        if meta.get("type") == "source":
                            found_title = meta.get("title")
                    except Exception:
                        pass
                
                # Check if it was just generated in this run
                if not found_title:
                    for rp in regular_pages:
                        if rp.metadata.type == "source" and rp.slug == stem:
                            found_title = rp.metadata.title
                            break

                if found_title:
                    paper_title = found_title
                else:
                    paper_title = stem.replace("-", " ").title()

            name = p.metadata.title
            if not name:
                name = p.slug.replace("-", " ").title()
            
            # Normalize name
            name = re.sub(r'\s+', ' ', name.strip()).title()

            # Parse affiliation from frontmatter
            affiliation = getattr(p.metadata, "affiliation", "") or "Unknown"

            raw_authors.append({
                "name": name,
                "affiliation": affiliation,
                "source_documents": p.metadata.source_documents,
                "paper_title": paper_title
            })

        # Deduplicate names
        to_remove = set()
        for i in range(len(raw_authors)):
            if i in to_remove: continue
            for j in range(len(raw_authors)):
                if i == j or j in to_remove: continue
                
                name_i = raw_authors[i]["name"]
                name_j = raw_authors[j]["name"]
                docs_i = set(raw_authors[i]["source_documents"])
                docs_j = set(raw_authors[j]["source_documents"])
                
                # Check if they share at least one source_document
                if docs_i.intersection(docs_j):
                    if name_i != name_j:
                        if name_i in name_j:
                            to_remove.add(i)
                            break
                        elif name_j in name_i:
                            to_remove.add(j)
                    else:
                        if i < j:
                            to_remove.add(j)

        deduped_authors = [raw_authors[i] for i in range(len(raw_authors)) if i not in to_remove]

        sections = {}
        for author in deduped_authors:
            paper_title = author["paper_title"]
            if paper_title not in sections:
                sections[paper_title] = []
            sections[paper_title].append({
                "name": author["name"],
                "affiliation": author["affiliation"]
            })

        if sections:
            self.wiki_repo.write_authors_page(workspace_id, sections)

        # Write all REGULAR pages to disk (no Gemini calls, pure file IO)
        for update in regular_pages:
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

        try:
            from datetime import date
            today = date.today().isoformat()
            current_index = self.wiki_repo.read_page_raw(workspace_id, "index.md")
            self.wiki_repo.write_overview_page(
                workspace_id=workspace_id,
                documents=parsed_docs,
                pages_created=pages_created,
                pages_updated=pages_updated,
                index_content=current_index,
                today=today,
            )
        except Exception as e:
            logger.warning(f"Overview update failed (non-critical): {e}")

        return IngestResult(
            pages_created=pages_created,
            pages_updated=pages_updated,
            summary=log_entry
        )

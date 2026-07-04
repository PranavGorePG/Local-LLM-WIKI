import os
from pydantic import BaseModel, Field
from typing import List, Optional, Set
from pathlib import Path
from app.core.logger import get_logger

logger = get_logger(__name__)

class GhostEntry(BaseModel):
    slug: str
    expected_path: str
    source_documents: List[str]   # filenames found in frontmatter, or []

class IntegrityReport(BaseModel):
    missing_folders_recreated: List[str] = Field(default_factory=list)
    index_rebuilt: bool = False
    ghost_entries: List[GhostEntry] = Field(default_factory=list)
    orphan_files: List[str] = Field(default_factory=list)
    recovered_pages: List[str] = Field(default_factory=list)
    stub_pages_created: List[str] = Field(default_factory=list)
    unrecoverable: List[str] = Field(default_factory=list)

WIKI_CATEGORY_FOLDERS = ["concepts", "entities", "topics", "sources"]
SYSTEM_PAGES = {"index.md", "log.md", "overview.md"}

class WikiIntegrityService:
    def __init__(self, wiki_repo, gemini, file_storage, parser, workspace_service):
        self.wiki_repo = wiki_repo
        self.gemini = gemini
        self.file_storage = file_storage
        self.parser = parser
        self.workspace_service = workspace_service

    def run_integrity_check(self, workspace_id: str) -> IntegrityReport:
        report = IntegrityReport()
        workspace_path = self.workspace_service.resolve_workspace_path(workspace_id)
        
        # STEP 1 — Folder Guard
        wiki_dir = self.wiki_repo._get_wiki_dir(workspace_id)
        if not wiki_dir.exists():
            wiki_dir.mkdir(parents=True, exist_ok=True)
            report.missing_folders_recreated.append("wiki")
            
        for folder in WIKI_CATEGORY_FOLDERS:
            folder_path = wiki_dir / folder
            if not folder_path.exists():
                folder_path.mkdir(parents=True, exist_ok=True)
                report.missing_folders_recreated.append(folder)

        # STEP 2 — Index Guard
        index_path = self.wiki_repo.get_page_path(workspace_id, "index.md")
        if not index_path.exists():
            self.wiki_repo.rebuild_index(workspace_id)
            report.index_rebuilt = True
            all_pages = self.wiki_repo.list_pages(workspace_id)
            report.orphan_files = [p for p in all_pages if p not in SYSTEM_PAGES]
            return report
            
        index_map = self.wiki_repo.parse_index(workspace_id)
        index_paths = {path for path in index_map.values() if path.endswith(".md") and path not in SYSTEM_PAGES}

        # STEP 3 — Cross-reference
        disk_files_list = self.wiki_repo.list_pages(workspace_id)
        disk_files = set(disk_files_list) - SYSTEM_PAGES
        ghost_paths = index_paths - disk_files
        report.orphan_files = list(disk_files - index_paths)

        for ghost_path in ghost_paths:
            slug = ghost_path.split("/")[-1].replace(".md", "")
            candidate_set: Set[str] = set()
            
            # Scan ALL existing wiki pages
            for disk_file in disk_files:
                try:
                    metadata, content = self.wiki_repo.read_page(workspace_id, disk_file)
                    if slug in metadata.get("related_pages", []) or f"[[{slug}]]" in content:
                        for doc in metadata.get("source_documents", []):
                            candidate_set.add(doc)
                except Exception as e:
                    logger.warning(f"Could not read {disk_file} during ghost resolution: {e}")
                    
            ghost_entry = GhostEntry(
                slug=slug,
                expected_path=ghost_path,
                source_documents=list(candidate_set)
            )
            report.ghost_entries.append(ghost_entry)

        # STEP 4 — Recovery for each ghost_entry
        for ghost_entry in report.ghost_entries:
            path_prefix = ghost_entry.expected_path.split("/")[0] if "/" in ghost_entry.expected_path else "topics"
            if path_prefix == "concepts":
                inferred_type = "concept"
            elif path_prefix == "entities":
                inferred_type = "entity"
            elif path_prefix == "sources":
                inferred_type = "source"
            else:
                inferred_type = "topic"

            # a) Resolve available raw files
            available_raws = []
            missing_raws = []
            
            if ghost_entry.source_documents:
                for filename in ghost_entry.source_documents:
                    try:
                        raw_path = self.file_storage.get_document_path(workspace_id, filename)
                        available_raws.append(raw_path)
                    except FileNotFoundError:
                        missing_raws.append(filename)
            else:
                # Fall back to all raw docs
                try:
                    all_docs = self.file_storage.list_documents(workspace_id)
                    for doc in all_docs:
                        raw_path = self.file_storage.get_document_path(workspace_id, doc.filename)
                        available_raws.append(raw_path)
                except Exception as e:
                    logger.warning(f"Could not list all documents for fallback: {e}")

            # b) Attempt recovery
            if available_raws:
                try:
                    parsed_docs = []
                    for raw_path in available_raws:
                        content = self.parser.parse_document(raw_path)
                        parsed_docs.append({"filename": raw_path.name, "content": content})
                        
                    concept_name = ghost_entry.slug.replace("-", " ").title()
                    
                    try:
                        with open(workspace_path / "AGENTS.md", "r", encoding="utf-8") as f:
                            agents_md = f.read()
                    except FileNotFoundError:
                        agents_md = ""
                        
                    page_updates = self.gemini.batch_compile_pages(
                        concepts=[{"concept_name": concept_name, "concept_type": inferred_type}],
                        existing_pages={concept_name: ""},
                        documents=parsed_docs,
                        agents_md=agents_md
                    )
                    
                    if page_updates:
                        self.wiki_repo.write_page(workspace_id, page_updates[0])
                        report.recovered_pages.append(ghost_entry.slug)
                        logger.info(f"Recovered ghost page: {ghost_entry.slug}")
                    else:
                        report.unrecoverable.append(ghost_entry.slug)
                except Exception as e:
                    logger.error(f"Error during recovery of {ghost_entry.slug}: {e}")
                    report.unrecoverable.append(ghost_entry.slug)
            
            # c) Build stub
            else:
                try:
                    title = ghost_entry.slug.replace("-", " ").title()
                    stub_md = f"---\ntitle: {title}\ntype: {inferred_type}\nsource_documents: []\ntags:\n  - stub\n  - source-unavailable\n---\n\n# ⚠️ Page Unavailable\n\nThis page was referenced in the index but its source documents are no\nlonger available. Manual reconstruction required.\n"
                    self.wiki_repo.write_page_raw(workspace_id, ghost_entry.expected_path, stub_md)
                    report.stub_pages_created.append(ghost_entry.slug)
                    logger.warning(f"Created stub for unrecoverable ghost page: {ghost_entry.slug}")
                except Exception as e:
                    logger.error(f"Error creating stub for {ghost_entry.slug}: {e}")
                    report.unrecoverable.append(ghost_entry.slug)

        # STEP 5 — Orphan note
        # Done in step 3, no action required.

        # STEP 6 — Always rebuild index at the end
        try:
            self.wiki_repo.rebuild_index(workspace_id)
        except Exception as e:
            logger.error(f"Error rebuilding index at end of integrity check: {e}")

        return report

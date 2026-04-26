import os
from pathlib import Path
from typing import List, Optional

from app.core.constants import WIKI_DIR_NAME, WIKI_CATEGORIES
from app.schemas.wiki import WikiPageUpdate, WikiPageMetadata
from app.services.workspace_service import WorkspaceService
from app.utils.frontmatter import parse_frontmatter, serialize_frontmatter
from app.utils.slug import generate_slug, ensure_md_extension
from app.core.logger import get_logger

logger = get_logger(__name__)

class WikiRepository:
    def __init__(self, workspace_service: WorkspaceService):
        self.workspace_service = workspace_service

    def _get_wiki_dir(self, workspace_id: str) -> Path:
        return self.workspace_service.resolve_workspace_path(workspace_id) / WIKI_DIR_NAME

    def get_page_path(self, workspace_id: str, relative_path: str) -> Path:
        wiki_dir = self._get_wiki_dir(workspace_id)
        # Prevent traversal
        path = (wiki_dir / relative_path).resolve()
        if not str(path).startswith(str(wiki_dir.resolve())):
            raise ValueError("Invalid path")
        return path

    def list_pages(self, workspace_id: str) -> List[str]:
        wiki_dir = self._get_wiki_dir(workspace_id)
        pages = []
        for root, dirs, files in os.walk(wiki_dir):
            for file in files:
                if file.endswith(".md"):
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(wiki_dir)
                    pages.append(str(rel_path).replace("\\", "/"))
        return pages

    def read_page(self, workspace_id: str, relative_path: str) -> tuple[dict, str]:
        path = self.get_page_path(workspace_id, relative_path)
        if not path.exists():
            raise FileNotFoundError(f"Page {relative_path} not found")
            
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            
        return parse_frontmatter(content)

    def write_page(self, workspace_id: str, update: WikiPageUpdate):
        wiki_dir = self._get_wiki_dir(workspace_id)
        
        page_type = update.metadata.type
        slug = ensure_md_extension(update.slug)
        
        if page_type == "index":
            rel_path = "index.md"
        elif page_type == "log":
            rel_path = "log.md"
        elif page_type == "overview":
            rel_path = "overview.md"
        elif page_type == "source":
            rel_path = f"sources/{slug}"
        elif page_type in [cat[:-1] for cat in WIKI_CATEGORIES] + WIKI_CATEGORIES:
            # handle 'concept' vs 'concepts'
            folder = page_type if page_type.endswith('s') else f"{page_type}s"
            if folder not in WIKI_CATEGORIES:
                folder = "topics"  # fallback
            rel_path = f"{folder}/{slug}"
        else:
            rel_path = f"topics/{slug}"
            
        path = self.get_page_path(workspace_id, rel_path)
        
        # Atomic write
        temp_path = path.with_suffix(".md.tmp")
        try:
            content_to_write = serialize_frontmatter(
                update.metadata.model_dump(exclude_none=True), 
                update.content
            )
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(content_to_write)
            temp_path.replace(path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise e

    def append_log(self, workspace_id: str, entry: str):
        path = self.get_page_path(workspace_id, "log.md")
        if path.exists():
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n{entry}\n")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: Log\ntype: log\n---\n\n# Log\n\n{entry}\n")

    def overwrite_index(self, workspace_id: str, content: str):
        path = self.get_page_path(workspace_id, "index.md")
        temp_path = path.with_suffix(".md.tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write("---\ntitle: Index\ntype: index\n---\n\n" + content)
            temp_path.replace(path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise e

from app.schemas.wiki import LintResult, LintIssue, WikiPageUpdate
from app.services.gemini_service import GeminiService
from app.services.wiki_repository import WikiRepository
from app.core.logger import get_logger
from pydantic import BaseModel
from typing import List

logger = get_logger(__name__)

class RepairResult(BaseModel):
    pages_repaired: int
    pages_deleted: int
    summary: str

class WikiRepairService:
    def __init__(self, gemini: GeminiService, wiki_repo: WikiRepository):
        self.gemini = gemini
        self.wiki_repo = wiki_repo

    def repair_wiki(self, workspace_id: str, lint_result: LintResult) -> RepairResult:
        # Load all page contents
        pages = self.wiki_repo.list_pages(workspace_id)
        
        pages_content = {}
        for path in pages:
            try:
                pages_content[path] = self.wiki_repo.read_page_raw(workspace_id, path)
            except Exception as e:
                logger.warning(f"Could not read page {path}: {e}")

        valid_slugs = [p.split("/")[-1].replace(".md", "") for p in pages]

        if not lint_result.issues:
            return RepairResult(
                pages_repaired=0,
                pages_deleted=0,
                summary="No issues to repair."
            )

        # Call Gemini once with all issues and all page contents
        result = self.gemini.repair_wiki(
            issues=lint_result.issues,
            pages_content=pages_content,
            valid_slugs=valid_slugs
        )

        # Write repaired/new pages
        pages_repaired = 0
        for update in result.pages:
            try:
                self.wiki_repo.write_page(workspace_id, update)
                pages_repaired += 1
            except Exception as e:
                logger.error(f"Error writing repaired page {update.slug}: {e}")

        # Delete confirmed duplicate pages
        pages_deleted = 0
        for path in result.pages_to_delete:
            try:
                full_path = self.wiki_repo.get_page_path(workspace_id, path)
                if full_path.exists():
                    full_path.unlink()
                    pages_deleted += 1
                    logger.info(f"Deleted duplicate page: {path}")
            except Exception as e:
                logger.error(f"Error deleting page {path}: {e}")

        # Rebuild index after repair
        self.wiki_repo.rebuild_index(workspace_id)

        return RepairResult(
            pages_repaired=pages_repaired,
            pages_deleted=pages_deleted,
            summary=f"Repaired {pages_repaired} pages, deleted {pages_deleted} duplicate pages."
        )

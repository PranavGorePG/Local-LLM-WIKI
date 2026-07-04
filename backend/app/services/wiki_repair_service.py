from app.schemas.wiki import LintResult, LintIssue, WikiPageUpdate
from app.services.gemini_service import GeminiService
from app.services.wiki_repository import WikiRepository
from app.services.wiki_integrity_service import IntegrityReport
from app.core.logger import get_logger
from pydantic import BaseModel
from typing import List, Optional

logger = get_logger(__name__)

CATEGORY_PREFIXES = ["topics/", "concepts/", "entities/", "sources/"]

class RepairResult(BaseModel):
    pages_repaired: int
    pages_deleted: int
    summary: str
    integrity: Optional[IntegrityReport] = None


def _sanitize_slug(slug: str) -> str:
    """Strip category prefix from slug if Gemini included it.
    e.g. 'topics/attention-score' → 'attention-score'
    """
    for prefix in CATEGORY_PREFIXES:
        if slug.startswith(prefix):
            return slug[len(prefix):]
    return slug


class WikiRepairService:
    def __init__(self, gemini: GeminiService, wiki_repo: WikiRepository, integrity_service):
        self.gemini = gemini
        self.wiki_repo = wiki_repo
        self.integrity_service = integrity_service

    def repair_wiki(self, workspace_id: str, lint_result: LintResult) -> RepairResult:
        # --- Integrity check first ---
        logger.info("Running integrity check before repair...")
        integrity_report = None
        try:
            integrity_report = self.integrity_service.run_integrity_check(workspace_id)
            if integrity_report.missing_folders_recreated:
                logger.info(f"Recreated folders: {integrity_report.missing_folders_recreated}")
            if integrity_report.index_rebuilt:
                logger.info("Index was missing and has been rebuilt.")
            if integrity_report.recovered_pages:
                logger.info(f"Recovered pages: {integrity_report.recovered_pages}")
            if integrity_report.stub_pages_created:
                logger.warning(f"Stub pages created (sources unavailable): {integrity_report.stub_pages_created}")
        except Exception as e:
            logger.error(f"Integrity check failed during repair: {e}")
            # Do not abort repair — continue with lint-based repair regardless

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
                # Sanitize slug — strip category prefix if Gemini included it
                update.slug = _sanitize_slug(update.slug)
                self.wiki_repo.write_page(workspace_id, update)
                pages_repaired += 1
                logger.info(f"Repaired page: {update.slug}")
            except Exception as e:
                logger.error(f"Error writing repaired page {update.slug}: {e}")

        # Delete confirmed duplicate pages
        pages_deleted = 0
        for path in result.pages_to_delete:
            try:
                # Normalize path separators for Windows compatibility
                path = path.replace("\\", "/")
                full_path = self.wiki_repo.get_page_path(workspace_id, path)
                if full_path.exists():
                    full_path.unlink()
                    pages_deleted += 1
                    logger.info(f"Deleted duplicate page: {path}")
                else:
                    logger.warning(f"Page marked for deletion not found on disk: {path}")
            except Exception as e:
                logger.error(f"Error deleting page {path}: {e}")

        # Rebuild index after repair
        try:
            self.wiki_repo.rebuild_index(workspace_id)
            logger.info("Index rebuilt after repair.")
        except Exception as e:
            logger.error(f"Error rebuilding index after repair: {e}")

        try:
            from datetime import date
            today = date.today().isoformat()
            overview_path = self.wiki_repo.get_page_path(workspace_id, "overview.md")

            if overview_path.exists():
                with open(overview_path, "r", encoding="utf-8") as f:
                    existing = f.read()

                new_line = (
                    f"- {today}: Repair — {pages_repaired} pages repaired, "
                    f"{pages_deleted} pages deleted\n"
                )

                if "## Recent Changes" in existing:
                    updated = existing.replace(
                        "## Recent Changes\n",
                        f"## Recent Changes\n{new_line}",
                        1  # replace only the first occurrence
                    )
                else:
                    updated = existing + f"\n## Recent Changes\n{new_line}"

                temp_path = overview_path.with_suffix(".md.tmp")
                with open(temp_path, "w", encoding="utf-8") as f:
                    f.write(updated)
                temp_path.replace(overview_path)

        except Exception as e:
            logger.warning(f"Overview repair update failed (non-critical): {e}")

        return RepairResult(
            pages_repaired=pages_repaired,
            pages_deleted=pages_deleted,
            summary=f"Repaired {pages_repaired} pages, deleted {pages_deleted} duplicate pages.",
            integrity=integrity_report
        )
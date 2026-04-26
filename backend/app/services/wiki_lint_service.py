import os
import re
from app.schemas.wiki import LintResult, LintIssue
from app.services.wiki_repository import WikiRepository

from app.services.gemini_service import GeminiService

class WikiLintService:
    def __init__(self, wiki_repo: WikiRepository, gemini_service: GeminiService):
        self.wiki_repo = wiki_repo
        self.gemini_service = gemini_service

    def lint_wiki(self, workspace_id: str) -> LintResult:
        issues = []
        pages = self.wiki_repo.list_pages(workspace_id)
        
        # Track valid links
        valid_slugs = []
        for p in pages:
            valid_slugs.append(p.split("/")[-1].replace(".md", ""))
            
        for path in pages:
            if path in ["index.md", "log.md", "overview.md"]:
                continue
                
            try:
                metadata, content = self.wiki_repo.read_page(workspace_id, path)
                
                # Check frontmatter
                if not metadata:
                    issues.append(LintIssue(severity="error", path=path, message="Missing YAML frontmatter"))
                else:
                    if "title" not in metadata:
                        issues.append(LintIssue(severity="error", path=path, message="Missing title in frontmatter"))
                    if "type" not in metadata:
                        issues.append(LintIssue(severity="error", path=path, message="Missing type in frontmatter"))
                        
                # Check empty
                if not content.strip():
                    issues.append(LintIssue(severity="warning", path=path, message="Page content is empty"))
                    
                # Check wikilinks
                links = re.findall(r"\[\[(.*?)\]\]", content)
                for link in links:
                    link_slug = link.split("|")[0]  # Handle [[link|alias]]
                    # Simple check, real Obsidian might be more complex
                    found = any(link_slug.lower() in p.lower() for p in pages)
                    if not found:
                        issues.append(LintIssue(severity="warning", path=path, message=f"Broken wikilink: [[{link}]]"))
                        
            except Exception as e:
                issues.append(LintIssue(severity="error", path=path, message=f"Error parsing page: {e}"))
                
        # Semantic Lint
        try:
            index_md = self.wiki_repo.read_page_raw(workspace_id, "index.md")
        except FileNotFoundError:
            index_md = ""
            
        pages_content = {}
        for path in pages:
            if path in ["index.md", "log.md", "overview.md"]:
                continue
            try:
                pages_content[path] = self.wiki_repo.read_page_raw(workspace_id, path)
            except FileNotFoundError:
                continue
                
        if index_md or pages_content:
            try:
                semantic_issues = self.gemini_service.semantic_lint(index_md, pages_content)
                issues.extend(semantic_issues)
            except Exception as e:
                issues.append(LintIssue(severity="error", path="semantic", message=f"Semantic lint failed: {e}"))
                
        return LintResult(issues=issues)

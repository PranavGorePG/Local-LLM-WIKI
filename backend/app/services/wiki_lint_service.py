import os
import re
from app.schemas.wiki import LintResult, LintIssue
from app.services.wiki_repository import WikiRepository

class WikiLintService:
    def __init__(self, wiki_repo: WikiRepository):
        self.wiki_repo = wiki_repo

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
                
        return LintResult(issues=issues)

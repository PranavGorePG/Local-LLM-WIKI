import os
import re
from pathlib import Path
from typing import List, Optional

from app.core.constants import WIKI_DIR_NAME, WIKI_CATEGORIES
from app.schemas.wiki import WikiPageUpdate, WikiPageMetadata
from app.services.workspace_service import WorkspaceService
from app.utils.frontmatter import parse_frontmatter, serialize_frontmatter
from app.utils.slug import generate_slug, ensure_md_extension
from app.core.logger import get_logger

logger = get_logger(__name__)

# ---------------------------------------------------------------------------
# Type → folder resolution
# ---------------------------------------------------------------------------

FOLDER_MAP = {
    # Canonical four types (singular and plural)
    "concept":   "concepts",
    "concepts":  "concepts",
    "entity":    "entities",
    "entities":  "entities",
    "person":    "entities",
    "topic":     "topics",
    "topics":    "topics",
    "source":    "sources",
    "sources":   "sources",
    # System page types — handled separately in write_page, listed here so
    # _resolve_folder() can short-circuit cleanly.
    "index":     None,
    "log":       None,
    "overview":  None,
}

# Keyword fragments → folder.
# Used ONLY when page_type is not in FOLDER_MAP.
# Order matters: more specific keywords come first.
FALLBACK_KEYWORD_MAP = {
    "entities": [
        "model",        # specific named model (BERT, GPT-4 …)
        "dataset",      # WMT 2014, ImageNet …
        "hardware",     # NVIDIA P100, TPU …
        "library",      # TensorFlow, PyTorch …
        "software",     # broader software products
        "framework",
        "benchmark",
        "paper",
        "organization",
        "system",
        "tool",
        "gpu",
        "corpus",
        "instrument",
    ],
    "concepts": [
        "architecture",     # model architecture, encoder-decoder architecture …
        "mechanism",        # attention mechanism …
        "technique",
        "method",
        "algorithm",
        "function",         # softmax, activation function …
        "regularization",   # dropout, label smoothing …
        "optimizer",        # adam, sgd …
        "encoding",         # positional encoding …
        "embedding",
        "strategy",         # decoding strategy …
        "component",        # model architecture component …
        "operation",
        "layer",
        "tokenization",
        "vocabulary",
        "connection",       # residual connection …
        "normalization",    # layer normalization …
        "network type",
        "objective",
        "loss",
        "metric",           # BLEU score, perplexity — debatable; treat as concept
        "score",
    ],
    "topics": [
        "task",             # machine translation, text classification …
        "field",
        "domain",
        "problem",
        "area",
        "subject",
        "application",
        "research",
        "decoding",
    ],
    "sources": [
        "source",
        "document",
        "publication",
        "paper",            # already in entities but "source paper" → sources
    ],
}


def _resolve_folder(page_type: str) -> str:
    """
    Map a page_type string (possibly free-form from Gemini) to a wiki
    category folder name: 'concepts' | 'entities' | 'topics' | 'sources'.

    Resolution order:
      1. Direct lookup in FOLDER_MAP  (exact, fast)
      2. Keyword scan in FALLBACK_KEYWORD_MAP  (handles Gemini creativity)
      3. Hard fallback → 'topics'
    """
    t = page_type.lower().strip()

    # 1. Direct match
    if t in FOLDER_MAP:
        result = FOLDER_MAP[t]
        return result if result is not None else "topics"

    # 2. Keyword match
    for folder, keywords in FALLBACK_KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword in t:
                logger.warning(
                    f"Unknown page_type '{page_type}' matched keyword "
                    f"'{keyword}' → routing to '{folder}'"
                )
                return folder

    # 3. Hard fallback
    logger.warning(
        f"Unknown page_type '{page_type}': no keyword match, defaulting to 'topics'"
    )
    return "topics"


# ---------------------------------------------------------------------------
# Repository
# ---------------------------------------------------------------------------

class WikiRepository:
    def __init__(self, workspace_service: WorkspaceService):
        self.workspace_service = workspace_service

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_wiki_dir(self, workspace_id: str) -> Path:
        return self.workspace_service.resolve_workspace_path(workspace_id) / WIKI_DIR_NAME

    def get_page_path(self, workspace_id: str, relative_path: str) -> Path:
        wiki_dir = self._get_wiki_dir(workspace_id)
        path = (wiki_dir / relative_path).resolve()
        if not str(path).startswith(str(wiki_dir.resolve())):
            raise ValueError("Invalid path — possible directory traversal")
        return path

    # ------------------------------------------------------------------
    # Read / list
    # ------------------------------------------------------------------

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

    def read_page_raw(self, workspace_id: str, relative_path: str) -> str:
        path = self.get_page_path(workspace_id, relative_path)
        if not path.exists():
            raise FileNotFoundError(f"Page {relative_path} not found")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def write_page(self, workspace_id: str, update: WikiPageUpdate):
        logger.info(f"write_page → slug='{update.slug}' type='{update.metadata.type}'")

        wiki_dir = self._get_wiki_dir(workspace_id)
        page_type = update.metadata.type.lower().strip()
        slug = ensure_md_extension(update.slug)

        # Resolve destination path
        if page_type == "index":
            rel_path = "index.md"
        elif page_type == "log":
            rel_path = "log.md"
        elif page_type == "overview":
            rel_path = "overview.md"
        else:
            folder = _resolve_folder(page_type)
            rel_path = f"{folder}/{slug}"

        path = self.get_page_path(workspace_id, rel_path)

        # Ensure parent directory exists (guards against deleted category folders)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Atomic write via temp file
        temp_path = path.with_suffix(".md.tmp")
        try:
            content_to_write = serialize_frontmatter(
                update.metadata.model_dump(exclude_none=True),
                update.content,
            )
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(content_to_write)
            temp_path.replace(path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise e

    def write_page_raw(self, workspace_id: str, relative_path: str, full_content: str):
        path = self.get_page_path(workspace_id, relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".md.tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(full_content)
            temp_path.replace(path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            raise e

    def write_authors_page(self, workspace_id: str, sections: dict[str, list[dict]]) -> None:
        import datetime
        path = self.get_page_path(workspace_id, "entities/authors.md")
        
        existing_sections = {}
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            
            parts = content.split("\n## ")
            for part in parts[1:]:
                lines = part.split("\n", 1)
                title = lines[0].strip()
                body = lines[1].strip() if len(lines) > 1 else ""
                existing_sections[title] = body

        for paper_title, authors in sections.items():
            section_lines = []
            section_lines.append("| Author | Affiliation |")
            section_lines.append("|--------|-------------|")
            for author in authors:
                name = author.get("name", "Unknown").strip()
                affil = author.get("affiliation", "").strip()
                if not affil:
                    affil = "Unknown"
                section_lines.append(f"| {name} | {affil} |")
            
            section_lines.append("")
            section_lines.append(f"> Source: {paper_title}")
            existing_sections[paper_title] = "\n".join(section_lines)
            
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        final_lines = [
            "---",
            "title: Authors",
            "type: entity",
            "tags: [authors, persons]",
            f"updated: {today}",
            "---",
            "",
            "# Authors"
        ]
        
        for paper_title, body in existing_sections.items():
            final_lines.append("")
            final_lines.append(f"## {paper_title}")
            final_lines.append("")
            final_lines.append(body)
            
        final_content = "\n".join(final_lines) + "\n"
        self.write_page_raw(workspace_id, "entities/authors.md", final_content)

    def write_overview_page(
        self,
        workspace_id: str,
        documents: list[dict],
        pages_created: int,
        pages_updated: int,
        index_content: str,
        today: str,
    ) -> None:
        sections = {"Concepts": 0, "Entities": 0, "Topics": 0, "Sources": 0}
        total_pages = 0
        current_section = None
        
        for line in index_content.splitlines():
            line = line.strip()
            if line.startswith("## "):
                sec_name = line[3:].strip()
                if sec_name in sections:
                    current_section = sec_name
                else:
                    current_section = None
            elif line.startswith("- [[") and current_section:
                sections[current_section] += 1
                total_pages += 1
                
        key_themes_bullets = []
        for sec_name, count in sections.items():
            if count > 0:
                key_themes_bullets.append(f"- **{sec_name}** — {count} pages")
        key_themes_str = "\n".join(key_themes_bullets)
        
        doc_count = len(documents)
        sources_table_lines = [
            "| Document | Ingested On |",
            "|---|---|"
        ]
        for doc in documents:
            sources_table_lines.append(f"| {doc['filename']} | {today} |")
        sources_table_str = "\n".join(sources_table_lines)
        
        source_paragraphs = []
        sources_dir = self._get_wiki_dir(workspace_id) / "sources"
        if sources_dir.exists() and sources_dir.is_dir():
            for md_file in sources_dir.glob("*.md"):
                try:
                    with open(md_file, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    if content.startswith("---\n"):
                        parts = content.split("---\n", 2)
                        if len(parts) >= 3:
                            fm_str = parts[1]
                            body = parts[2]
                            
                            title = "Unknown Source"
                            for f_line in fm_str.splitlines():
                                if f_line.startswith("title:"):
                                    title = f_line[6:].strip()
                                    break
                                    
                            lines = body.splitlines()
                            para_lines = []
                            for ln in lines:
                                ln_stripped = ln.strip()
                                if ln_stripped.startswith("# ") and not para_lines:
                                    continue
                                if ln_stripped.startswith("## "):
                                    break
                                if not ln_stripped:
                                    if para_lines:
                                        break
                                    continue
                                para_lines.append(ln_stripped)
                                
                            para = " ".join(para_lines)
                            if len(para) > 300:
                                para = para[:300].rstrip() + "..."
                                
                            if para:
                                source_paragraphs.append(f"**{title}** — {para}")
                except Exception as e:
                    logger.warning(f"Could not read source page {md_file} for overview: {e}")
                    
        if source_paragraphs:
            source_desc_str = "\n\n".join(source_paragraphs)
        else:
            source_desc_str = f"This workspace contains {total_pages} wiki pages compiled from {doc_count} source document(s)."
            
        overview_path = self.get_page_path(workspace_id, "overview.md")
        existing_history_lines = ""
        if overview_path.exists():
            try:
                with open(overview_path, "r", encoding="utf-8") as f:
                    overview_content = f.read()
                if "## Recent Changes" in overview_content:
                    existing_history_lines = overview_content.split("## Recent Changes")[1].strip()
            except Exception as e:
                logger.warning(f"Could not read existing overview page history: {e}")
                
        new_entry = f"- {today}: Ingest — {pages_created} pages created, {pages_updated} pages updated"
        
        if existing_history_lines:
            history_str = new_entry + "\n" + existing_history_lines
        else:
            history_str = new_entry
            
        final_content = f"""---
title: Overview
type: overview
updated: {today}
---

# Workspace Overview

## Summary
This workspace contains {total_pages} wiki pages compiled from {doc_count} source document(s).

{source_desc_str}

## Key Themes
{key_themes_str}

## Sources Ingested
{sources_table_str}

## Authors
See [[authors]] for the full compiled author list.

## Recent Changes
{history_str}
"""
        self.write_page_raw(workspace_id, "overview.md", final_content)

    # ------------------------------------------------------------------
    # Index
    # ------------------------------------------------------------------

    def parse_index(self, workspace_id: str) -> dict:
        """
        Returns a unified lookup dict:
            slug        → relative_path   (e.g. "neural-network" → "concepts/neural-network.md")
            title       → relative_path   (e.g. "Neural Network" → "concepts/neural-network.md")

        Having both keys lets wiki_compiler_service find existing pages whether
        it's searching by Gemini-returned concept_name ("Neural Network") or by
        the slug stored in the index ("neural-network").
        """
        try:
            path = self.get_page_path(workspace_id, "index.md")
            if not path.exists():
                return {}

            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

            index_map: dict = {}
            matches = re.findall(r"-\s+\[\[(.*?)\]\]\s+→\s+([\w/.\-]+\.md)", content)

            # Pass 1 — slug → path
            for slug, rel_path in matches:
                index_map[slug] = rel_path

            # Pass 2 — frontmatter title → path  (enables concept_name lookup)
            for slug, rel_path in matches:
                try:
                    metadata, _ = self.read_page(workspace_id, rel_path)
                    title = metadata.get("title", "").strip()
                    if title and title not in index_map:
                        index_map[title] = rel_path
                except FileNotFoundError:
                    logger.warning(
                        f"parse_index: page listed in index not found on disk: {rel_path}"
                    )
                except Exception as e:
                    logger.warning(f"parse_index: could not read title for {rel_path}: {e}")

            return index_map

        except Exception as e:
            logger.error(f"parse_index failed: {e}")
            return {}

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

    def rebuild_index(self, workspace_id: str):
        """
        Walk every .md file in the wiki, read frontmatter, and regenerate
        index.md grouped by category.

        Uses _resolve_folder() for type→category mapping so the index always
        reflects the same routing logic as write_page().
        """
        pages = self.list_pages(workspace_id)

        grouped: dict[str, list[str]] = {
            "concepts": [],
            "entities": [],
            "topics":   [],
            "sources":  [],
        }

        SYSTEM_PAGES = {"index.md", "log.md", "overview.md"}

        for path in pages:
            if path in SYSTEM_PAGES:
                continue

            try:
                metadata, _ = self.read_page(workspace_id, path)
            except FileNotFoundError:
                logger.warning(f"rebuild_index: page file missing, skipping: {path}")
                continue
            except Exception as e:
                logger.warning(f"rebuild_index: could not read {path}: {e}")
                continue

            if not metadata:
                logger.warning(f"rebuild_index: no frontmatter in {path}, skipping")
                continue

            p_type = metadata.get("type", "topic")
            if p_type.lower().strip() == "person":
                continue
                
            category = _resolve_folder(p_type)

            # _resolve_folder never returns None for non-system types,
            # but guard anyway.
            if category not in grouped:
                category = "topics"

            slug = path.split("/")[-1].replace(".md", "")
            grouped[category].append(f"- [[{slug}]] → {path}")

        body = (
            "# Index\n\n"
            "Welcome to the wiki index.\n\n"
            "<!--\n"
            "ENFORCED INDEX FORMAT:\n"
            "- [[slug]] → category/slug.md\n"
            "-->\n\n"
        )

        for cat in ["concepts", "entities", "topics", "sources"]:
            if grouped[cat]:
                body += f"## {cat.capitalize()}\n"
                for entry in sorted(grouped[cat]):
                    body += f"{entry}\n"
                body += "\n"

        self.overwrite_index(workspace_id, body)

    # ------------------------------------------------------------------
    # Log
    # ------------------------------------------------------------------

    def append_log(self, workspace_id: str, entry: str):
        path = self.get_page_path(workspace_id, "log.md")
        if path.exists():
            with open(path, "a", encoding="utf-8") as f:
                f.write(f"\n{entry}\n")
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: Log\ntype: log\n---\n\n# Log\n\n{entry}\n")
import json
import time
from typing import List
from google import genai
from google.genai import types
from pydantic import BaseModel

from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.wiki import WikiPageUpdate
from app.schemas.chat import ChatMessage, ChatResponse, Citation

logger = get_logger(__name__)


# Pydantic schemas for Gemini Structured Outputs
class IngestResponseSchema(BaseModel):
    pages: List[WikiPageUpdate]
    index_markdown: str
    log_entry: str
    summary: str

class BatchCompileResponse(BaseModel):
    pages: List[WikiPageUpdate]

class ConceptExtractionSchema(BaseModel):
    concept_name: str
    concept_type: str

class ExtractionResponseSchema(BaseModel):
    concepts: List[ConceptExtractionSchema]

from app.schemas.wiki import LintIssue
class SemanticLintResponseSchema(BaseModel):
    issues: List[LintIssue]

class RepairResponseSchema(BaseModel):
    pages: List[WikiPageUpdate]
    pages_to_delete: List[str]  # relative paths to delete e.g. "topics/duplicate.md"

class QueryRoutingSchema(BaseModel):
    relevant_page_paths: List[str]


class QueryAnswerSchema(BaseModel):
    answer: str
    citations: List[Citation]
    insufficient_coverage: bool
    is_insightful: bool
    insight_summary: str


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL
        self._min_interval = 4.0  # seconds between calls
        self._last_call_time = 0.0

    def _rate_limit(self):
        now = time.time()
        elapsed = now - self._last_call_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_call_time = time.time()

    def compile_wiki_updates(
        self,
        agents_md: str,
        current_index: str,
        page_catalog: str,
        documents: List[dict],
    ) -> IngestResponseSchema:
        prompt = f"""
You are a knowledge compiler. Your task is to ingest new documents and generate updates to a Markdown Wiki.
The Wiki must be Obsidian-compatible.

WORKSPACE CONTEXT (AGENTS.md):
{agents_md}

CURRENT INDEX:
{current_index}

EXISTING PAGE CATALOG:
{page_catalog}

RAW DOCUMENTS TO INGEST:
"""
        for doc in documents:
            prompt += f"\n\n--- Document: {doc['filename']} ---\n{doc['content']}\n"

        prompt += """
INSTRUCTIONS:
1. Extract concepts, entities, topics, and source summaries from the raw documents.
2. Create or update Wiki pages. If a topic already exists in the catalog, output the full updated content, merging new information. Do NOT create duplicates.
3. Use [[wikilinks]] for all internal references within page content.
4. Provide stable slugs for filenames (e.g., "my-concept").
5. Generate a completely rewritten index in markdown format reflecting all pages (existing and new). Group them by type (Concepts, Entities, Topics, Sources).
6. Provide a short log entry summarizing what was ingested.
7. Provide a short overall summary.
8. Return raw JSON only. Do NOT wrap it in markdown code blocks.
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a strict JSON-emitting API.",
                    response_mime_type="application/json",
                    response_schema=IngestResponseSchema,
                ),
            )
            data = json.loads(response.text)
            return IngestResponseSchema.model_validate(data)
        except Exception as e:
            logger.error(f"Gemini compile error: {e}")
            raise

    def route_query(self, query: str, page_catalog: str) -> List[str]:
        prompt = f"""
Given the user question and the wiki catalog, select the paths of the pages most likely to contain the answer.
Select ONLY from the provided catalog paths. Keep the selection minimal.

QUESTION:
{query}

CATALOG:
{page_catalog}
"""

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=QueryRoutingSchema,
                ),
            )
            data = json.loads(response.text)
            return QueryRoutingSchema.model_validate(data).relevant_page_paths
        except Exception as e:
            logger.error(f"Gemini routing error: {e}")
            raise

    def answer_query(
        self, history: List[ChatMessage], wiki_context: str
    ) -> QueryAnswerSchema:
        system_instruction = (
            "You are a helpful knowledge assistant. Answer the user's question using ONLY the provided Wiki context.\n"
            "If the context does not contain the answer, say so clearly and set insufficient_coverage to true.\n"
            "Return your response in JSON format including citations to the used wiki pages.\n\n"
            "IMPORTANT: Evaluate your answer for novel insight.\n"
            "- Set is_insightful=True ONLY if your answer contains a novel connection, comparative synthesis, or conclusion not explicitly stated in any single wiki page.\n"
            "- Set is_insightful=False for simple factual lookups, insufficient coverage responses, or conversational exchanges.\n"
            "- If is_insightful=True, provide a concise paragraph in insight_summary summarizing the novel insight suitable for filing back into the wiki. Otherwise, leave it empty.\n\n"
            f"WIKI CONTEXT:\n{wiki_context}"
        )

        # Build contents list from full conversation history
        contents = []
        for msg in history:
            role = "user" if msg.role == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg.content)],
                )
            )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=QueryAnswerSchema,
                ),
            )
            data = json.loads(response.text)
            return QueryAnswerSchema.model_validate(data)
        except Exception as e:
            logger.error(f"Gemini answer error: {e}")
            raise

    def extract_concepts(self, documents: List[dict]) -> List[dict]:
        prompt = "Extract key concepts, entities, topics, and sources from these documents.\n"
        prompt += """
DEDUPLICATION RULES — strictly follow these:
- Always use the singular canonical form of a concept. "Neural Networks" becomes "Neural Network". "Recurrent Neural Networks (RNNs)" becomes "Recurrent Neural Network (RNN)".
- If two concepts refer to the same real-world thing, return only one entry for them using the most common canonical name.
- Never return abbreviations and their expansions as separate concepts. "RNN" and "Recurrent Neural Network" are the same concept — return only the full expanded form.
- Never return both a concept and its plural form. Always prefer singular.
- Before finalizing the list, review it and remove any duplicates or near-duplicates.
"""
        for doc in documents:
            prompt += f"\n--- Document: {doc['filename']} ---\n{doc['content']}\n"
            
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=ExtractionResponseSchema,
                ),
            )
            data = json.loads(response.text)
            return data.get("concepts", [])
        except Exception as e:
            logger.error(f"Gemini extraction error: {e}")
            raise

    def batch_compile_pages(
        self,
        concepts: List[dict],
        existing_pages: dict,
        documents: List[dict],
        agents_md: str
    ) -> List[WikiPageUpdate]:
        prompt = f"""
        You are a wiki page compiler. Given a list of concepts and raw documents, produce one wiki page per concept.
        
        WORKSPACE CONTEXT (AGENTS.md):
        {agents_md}
        
        For each concept:
        - If existing_page_content is provided for it, MERGE the new document information into it. Preserve all existing verified content. Integrate new information into relevant sections. Flag contradictions explicitly with a `> ⚠️ Contradiction:` blockquote. Update source_documents in frontmatter.
        - If no existing_page_content is provided, CREATE a new wiki page for it from scratch.
        
        All pages must:
        - Have YAML frontmatter with title, type, source_documents, related_pages, tags
        - Use [[wikilinks]] for all internal concept references
        - Have stable slugs
        
        IMPORTANT: If you notice two concepts in the input list that refer to the same thing, merge them into a single page. Do not produce two separate WikiPageUpdate objects for the same real-world concept.
        
        Return a JSON array of WikiPageUpdate objects, one per concept.
        """
        
        prompt += "\n\nRAW DOCUMENTS:\n"
        for doc in documents:
            prompt += f"--- Document: {doc['filename']} ---\n{doc['content']}\n\n"
            
        prompt += "\nCONCEPTS TO COMPILE:\n"
        for concept in concepts:
            name = concept['concept_name']
            ctype = concept['concept_type']
            existing_content = existing_pages.get(name, "")
            
            prompt += f"--- Concept: {name} (Type: {ctype}) ---\n"
            if existing_content:
                prompt += f"EXISTING PAGE CONTENT:\n{existing_content}\n"
            else:
                prompt += "NEW PAGE (No existing content)\n"
            prompt += "\n"
            
        try:
            self._rate_limit()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=BatchCompileResponse,
                ),
            )
            data = json.loads(response.text)
            return BatchCompileResponse.model_validate(data).pages
        except Exception as e:
            logger.error(f"Gemini batch_compile error: {e}")
            raise

    def semantic_lint(self, index_md: str, pages_content: dict) -> List[LintIssue]:
        prompt = f"""
        Perform a semantic lint on the entire wiki.
        Analyze the wiki holistically and return a list of semantic issues.
        
        Issues to detect: 
        - contradictions between pages
        - stale claims superseded by newer sources
        - orphan pages with no inbound links
        - important concepts mentioned but lacking their own page
        - missing cross-references between related pages
        - data gaps that could be filled
        
        Also suggest new questions to investigate and new sources to look for (use severity: "suggestion").
        
        INDEX:
        {index_md}
        
        PAGES CONTENT:
        """
        for path, content in pages_content.items():
            prompt += f"\n--- Page: {path} ---\n{content}\n"
            
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=SemanticLintResponseSchema,
                ),
            )
            data = json.loads(response.text)
            return SemanticLintResponseSchema.model_validate(data).issues
        except Exception as e:
            logger.error(f"Gemini semantic_lint error: {e}")
            raise

    def merge_insight_into_page(self, existing_page_content: str, insight_summary: str, page_path: str) -> str:
        prompt = f"""
        You are a knowledge curator. Merge the novel insight into the existing wiki page naturally.
        
        INSTRUCTIONS:
        - Preserve ALL existing content and the YAML frontmatter exactly as it is.
        - Add the insight as a new section or extend relevant sections naturally.
        - Return the full updated page content as a complete markdown string (including the original frontmatter).
        
        INSIGHT TO ADD:
        {insight_summary}
        
        EXISTING PAGE CONTENT:
        {existing_page_content}
        """
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig()
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini merge_insight error: {e}")
            raise

    def repair_wiki(
        self,
        issues: List[LintIssue],
        pages_content: dict,
        valid_slugs: List[str]
    ) -> RepairResponseSchema:
        prompt = f"""
        You are a wiki repair agent. You have been given a list of lint issues and the full content of all wiki pages.
        Your job is to fix all issues and return the corrected pages.
        
        ISSUES TO FIX:
        {issues}
        
        ALL CURRENT WIKI PAGES:
        {pages_content}
        
        VALID EXISTING SLUGS:
        {valid_slugs}
        
        REPAIR INSTRUCTIONS:
        
        1. DUPLICATE PAGES — For every pair of duplicate or near-duplicate pages flagged:
           - Merge their content into one single comprehensive page
           - Use the simpler canonical slug (e.g. prefer "recurrent-neural-network" over "recurrent-neural-network-rnn")
           - Add the duplicate's path to pages_to_delete
           - Update all wikilinks in other pages that referenced the deleted slug to point to the canonical slug
        
        2. BROKEN WIKILINKS — For every broken wikilink flagged:
           - Find the closest matching page from valid_slugs
           - Update the wikilink in the page to use the correct slug
           - If no matching page exists, remove the wikilink brackets and leave it as plain text
        
        3. STALE CLAIMS — For every stale claim flagged:
           - Update the relevant section of the page with accurate current information
           - Preserve all other content on the page
        
        4. MISSING CROSS REFERENCES — For every missing cross-reference flagged:
           - Add the appropriate [[wikilink]] in the relevant section of the page
        
        5. ORPHAN PAGES — For every orphan page flagged:
           - Add appropriate [[wikilinks]] to it from related pages
        
        6. SUGGESTIONS (severity: suggestion) — implement only if straightforward:
           - Create new suggested pages if the suggestion is to add a missing concept page
           - Skip suggestions that require external research or web search
        
        RULES:
        - Preserve all existing frontmatter fields. Only update content and wikilinks.
        - Never delete a page unless it is a confirmed duplicate with its content merged elsewhere.
        - Always use [[wikilinks]] for internal references.
        - Return only pages that have actually changed plus any new pages created.
        - Do not return unchanged pages.
        - pages_to_delete must only contain paths of duplicates whose content has been fully merged.
        """
        try:
            self._rate_limit()
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=RepairResponseSchema,
                ),
            )
            data = json.loads(response.text)
            return RepairResponseSchema.model_validate(data)
        except Exception as e:
            logger.error(f"Gemini repair_wiki error: {e}")
            raise
from app.schemas.wiki import LintIssue
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


# ---------------------------------------------------------------------------
# Pydantic schemas for Gemini Structured Outputs
# ---------------------------------------------------------------------------

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


class SemanticLintResponseSchema(BaseModel):
    issues: List[LintIssue]


class RepairResponseSchema(BaseModel):
    pages: List[WikiPageUpdate]
    pages_to_delete: List[str]  # relative paths e.g. "topics/duplicate.md"


class QueryRoutingSchema(BaseModel):
    relevant_page_paths: List[str]


class QueryAnswerSchema(BaseModel):
    answer: str
    citations: List[Citation]
    insufficient_coverage: bool
    is_insightful: bool
    insight_summary: str


# ---------------------------------------------------------------------------
# Shared prompt fragments
# Single source of truth — both extract_concepts and batch_compile_pages
# reference the same rules so Gemini's output is always consistent.
# ---------------------------------------------------------------------------

_TYPE_CONSTRAINT_BLOCK = """
CRITICAL — concept_type / frontmatter "type" field MUST be exactly one of these
four values. No other values are accepted.

  "concept"  → Abstract ideas, techniques, methods, mechanisms, algorithms,
               model architectures (generic), mathematical operations,
               training strategies, regularization methods, optimizers,
               encodings, functions, model components (attention, normalization,
               residual connections, feed-forward layers, embeddings…)

  "entity"   → Specific NAMED things that exist in the real world:
               named models        (Transformer, BERT, GPT-4)
               named datasets      (WMT 2014, ImageNet, Penn Treebank)
               named hardware      (NVIDIA P100, Google TPU v3)
               named software      (TensorFlow, PyTorch, Tensor2Tensor)
               named organizations (Google Brain, OpenAI, DeepMind)
               named people/authors (Ashish Vaswani, Noam Shazeer)
               named venues        (NeurIPS 2017, ICML 2024)
               named benchmarks    (GLUE, SuperGLUE)

  "topic"    → Broad subject areas, research fields, problem domains, tasks:
               machine translation, natural language processing,
               sequence modeling, image classification, speech recognition

  "source"   → The document / paper / book being ingested itself

  "person"   → A human individual — paper authors, researchers, reviewers,
               or any named person mentioned in the documents.
               Examples: Ashish Vaswani, Geoffrey Hinton, Yann LeCun

MAPPING GUIDE — use this when in doubt:
  model architecture (generic concept)      → "concept"
  attention mechanism                       → "concept"
  technique / method / algorithm            → "concept"
  optimizer algorithm (Adam, SGD)           → "concept"
  regularization (dropout, label smoothing) → "concept"
  mathematical function (softmax, ReLU)     → "concept"
  tokenization method (BPE, WordPiece)      → "concept"
  model component (FFN, layer norm…)        → "concept"
  named model    (Transformer, BERT)        → "entity"
  named dataset  (WMT 2014)                → "entity"
  named hardware (NVIDIA P100)             → "entity"
  named library  (Tensor2Tensor)           → "entity"
  named venue    (NeurIPS 2017)            → "entity"
  named author / researcher / reviewer      → "person"
  any named human individual                → "person"
  task / problem domain                    → "topic"
  research field / broad area              → "topic"
  paper / book being ingested              → "source"

DO NOT invent new type values. ONLY "concept", "entity", "topic", "source", "person" are valid.
"""

_SLUG_RULES_BLOCK = """
SLUG RULES — strictly follow these when setting the "slug" field:
  - Derive the slug ONLY from the concept/entity name. NEVER append the type.
  - Use lowercase letters and hyphens only. No underscores, no special characters.
  - Keep it concise — use the shortest unambiguous form.
  - For names with common abbreviations, use the full expanded name only.

  CORRECT examples:
    "Transformer"                          → slug: "transformer"
    "Adam Optimizer"                       → slug: "adam-optimizer"
    "Recurrent Neural Network"             → slug: "recurrent-neural-network"
    "Multi-Head Attention"                 → slug: "multi-head-attention"
    "WMT 2014 English-German"              → slug: "wmt-2014-english-german"
    "Ashish Vaswani"                       → slug: "ashish-vaswani"
    "NeurIPS 2017"                         → slug: "neurips-2017"
    "BLEU Score"                           → slug: "bleu-score"

  WRONG examples — DO NOT produce these:
    "adam-optimizer-optimizer"             ✗ type appended
    "transformer-model-architecture"       ✗ type appended
    "recurrent-neural-network-rnn"         ✗ abbreviation appended
    "multi-head-attention-model-component" ✗ type appended
    "bleu-score-metric"                    ✗ type appended
"""

_DEDUP_RULES_BLOCK = """
DEDUPLICATION RULES:
  - Always use the singular canonical form. "Neural Networks" → "Neural Network".
  - Never return an abbreviation and its expansion as separate entries.
    "RNN" and "Recurrent Neural Network" are the same — return only the full form.
  - Never return both a concept and its plural. Always prefer singular.
  - Review the full output list before finalising and remove duplicates /
    near-duplicates.
  - If two concepts refer to the same real-world thing, produce ONE entry using
    the most common canonical name.
"""

_ACADEMIC_PAPER_BLOCK = """
ACADEMIC PAPER EXTRACTION — always extract ALL of the following from research papers:

  1. The paper itself as type "source"
     concept_name: full paper title  (e.g. "Attention Is All You Need")
     slug: derived from title        (e.g. "attention-is-all-you-need")

  2. Every named author as type "person"
     Extract ALL authors listed, including less prominent ones.
     Examples: "Ashish Vaswani", "Noam Shazeer", "Niki Parmar",
               "Jakob Uszkoreit", "Llion Jones", "Aidan N. Gomez",
               "Lukasz Kaiser", "Illia Polosukhin"

  3. Named institution / affiliation as type "entity"
     Examples: "Google Brain", "Google Research", "University of Toronto"

  4. Named conference / journal / venue as type "entity"
     Examples: "NeurIPS 2017", "ICML 2024", "Journal of Machine Learning Research"
"""


# ---------------------------------------------------------------------------
# Service
# ---------------------------------------------------------------------------

class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL
        self._min_interval = 4.0   # minimum seconds between API calls
        self._last_call_time = 0.0

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _rate_limit(self):
        """Enforce minimum interval between Gemini API calls."""
        now = time.time()
        elapsed = now - self._last_call_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_call_time = time.time()

    def _generate(self, **kwargs):
        """
        Central wrapper around generate_content.
        - Applies rate limiting before EVERY call (fixes the bug where only
          batch_compile_pages and repair_wiki called _rate_limit).
        - Retries once on 429 / quota errors with doubled wait time.
        """
        self._rate_limit()
        try:
            return self.client.models.generate_content(**kwargs)
        except Exception as e:
            err_str = str(e).lower()
            if "429" in err_str or "quota" in err_str or "rate" in err_str:
                wait = self._min_interval * 2
                logger.warning(f"Rate limit hit — waiting {wait}s before retry")
                time.sleep(wait)
                self._last_call_time = time.time()
                return self.client.models.generate_content(**kwargs)
            raise

    # ------------------------------------------------------------------
    # Public API methods
    # ------------------------------------------------------------------

    def compile_wiki_updates(
        self,
        agents_md: str,
        current_index: str,
        page_catalog: str,
        documents: List[dict],
    ) -> IngestResponseSchema:
        prompt = f"""You are a knowledge compiler. Ingest the provided documents and
generate updates to a Markdown Wiki. The Wiki must be Obsidian-compatible.

WORKSPACE CONTEXT (AGENTS.md):
{agents_md}

CURRENT INDEX:
{current_index}

EXISTING PAGE CATALOG:
{page_catalog}

{_TYPE_CONSTRAINT_BLOCK}

{_SLUG_RULES_BLOCK}

{_DEDUP_RULES_BLOCK}

{_ACADEMIC_PAPER_BLOCK}

RAW DOCUMENTS TO INGEST:
"""
        for doc in documents:
            prompt += f"\n\n--- Document: {doc['filename']} ---\n{doc['content']}\n"

        prompt += """

INSTRUCTIONS:
1. Extract concepts, entities, topics and source summaries from the raw documents.
2. Create or update Wiki pages. If a topic already exists in the catalog, output
   the full updated content merging new information. Do NOT create duplicates.
3. Use [[wikilinks]] for all internal references within page content.
4. Generate a completely rewritten index in markdown format reflecting all pages
   (existing and new). Group them by type (Concepts, Entities, Topics, Sources).
5. Provide a short log entry summarising what was ingested.
6. Provide a short overall summary.
7. Return raw JSON only. Do NOT wrap it in markdown code blocks.
"""
        try:
            response = self._generate(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction="You are a strict JSON-emitting API.",
                    response_mime_type="application/json",
                    response_schema=IngestResponseSchema,
                    max_output_tokens=65536,
                ),
            )
            data = json.loads(response.text)
            return IngestResponseSchema.model_validate(data)
        except Exception as e:
            logger.error(f"Gemini compile_wiki_updates error: {e}")
            raise

    def route_query(self, query: str, page_catalog: str) -> List[str]:
        prompt = f"""Given the user question and the wiki catalog, select the paths of
the pages most likely to contain the answer.
Select ONLY from the provided catalog paths. Keep the selection minimal and relevant.

QUESTION:
{query}

CATALOG:
{page_catalog}
"""
        try:
            response = self._generate(
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
            logger.error(f"Gemini route_query error: {e}")
            raise

    def answer_query(
        self, history: List[ChatMessage], wiki_context: str
    ) -> QueryAnswerSchema:
        system_instruction = (
            "You are a helpful knowledge assistant. Answer the user's question using "
            "ONLY the provided Wiki context.\n"
            "If the context does not contain the answer, say so clearly and set "
            "insufficient_coverage to true.\n"
            "Return your response in JSON format including citations to the used "
            "wiki pages.\n\n"
            "IMPORTANT: Evaluate your answer for novel insight.\n"
            "- Set is_insightful=True ONLY if your answer contains a novel connection, "
            "comparative synthesis, or conclusion not explicitly stated in any single "
            "wiki page.\n"
            "- Set is_insightful=False for simple factual lookups, insufficient "
            "coverage responses, or conversational exchanges.\n"
            "- If is_insightful=True, provide a concise paragraph in insight_summary "
            "summarising the novel insight suitable for filing back into the wiki. "
            "Otherwise leave it empty.\n\n"
            f"WIKI CONTEXT:\n{wiki_context}"
        )

        contents = []
        for msg in history:
            role = "user" if msg.role == "user" else "model"
            contents.append(
                types.Content(role=role, parts=[types.Part(text=msg.content)])
            )

        try:
            response = self._generate(
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
            logger.error(f"Gemini answer_query error: {e}")
            raise

    def extract_concepts(self, documents: List[dict], chunk_size: int = 2) -> List[dict]:
        all_concepts = []

        base_prompt = f"""Extract every meaningful concept, entity, topic, and source from
the documents provided below.

{_TYPE_CONSTRAINT_BLOCK}

{_SLUG_RULES_BLOCK}

{_DEDUP_RULES_BLOCK}

{_ACADEMIC_PAPER_BLOCK}
"""
        
        for i in range(0, len(documents), chunk_size):
            chunk = documents[i:i + chunk_size]
            prompt = base_prompt
            for doc in chunk:
                prompt += f"\n--- Document: {doc['filename']} ---\n{doc['content']}\n"

            try:
                response = self._generate(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=ExtractionResponseSchema,
                        max_output_tokens=65536,
                    ),
                )
                data = json.loads(response.text)
                all_concepts.extend(data.get("concepts", []))
            except Exception as e:
                logger.error(f"Gemini extract_concepts error on chunk: {e}")
                raise

        type_priority = {
            "person": 4,
            "entity": 3,
            "concept": 2,
            "topic": 1,
            "source": 1
        }
        
        deduped = {}
        for concept in all_concepts:
            name = concept.get("concept_name", "")
            norm_name = name.lower().strip()
            if not norm_name:
                continue
                
            curr_type = concept.get("concept_type", "concept")
            
            if norm_name not in deduped:
                deduped[norm_name] = concept
            else:
                existing_type = deduped[norm_name].get("concept_type", "concept")
                if type_priority.get(curr_type, 0) > type_priority.get(existing_type, 0):
                    deduped[norm_name] = concept
                    
        return list(deduped.values())

    def batch_compile_pages(
        self,
        concepts: List[dict],
        existing_pages: dict,
        documents: List[dict],
        agents_md: str,
        chunk_size: int = 10,
    ) -> List[WikiPageUpdate]:
        all_updates = []

        base_prompt = f"""You are a wiki page compiler. Given a list of concepts and raw
documents, produce one wiki page per concept.

WORKSPACE CONTEXT (AGENTS.md):
{agents_md}

{_TYPE_CONSTRAINT_BLOCK}

{_SLUG_RULES_BLOCK}

For each concept:
- If existing_page_content is provided, MERGE new information into it.
  Preserve all existing verified content. Integrate new information into relevant
  sections. Flag contradictions explicitly with a `> ⚠️ Contradiction:` blockquote.
  Update source_documents in frontmatter.
- If no existing_page_content is provided, CREATE a new wiki page from scratch.

All pages must:
- Have YAML frontmatter with: title, type, source_documents, related_pages, tags
- For pages of type 'person', the YAML frontmatter must include an 'affiliation' field containing the person's institutional affiliation as a plain text string. If the affiliation is unknown or not mentioned in the documents, set it to an empty string. Example: affiliation: Google Brain
- Use [[wikilinks]] for all internal concept references
- Have a slug that follows the SLUG RULES above exactly

IMPORTANT: If two concepts in the input list refer to the same real-world thing,
merge them into a single WikiPageUpdate. Do not produce two separate objects for
the same concept.

Return a JSON array of WikiPageUpdate objects, one per (deduplicated) concept.

RAW DOCUMENTS:
"""
        for doc in documents:
            base_prompt += f"--- Document: {doc['filename']} ---\n{doc['content']}\n\n"

        for i in range(0, len(concepts), chunk_size):
            chunk = concepts[i:i + chunk_size]
            prompt = base_prompt + "\nCONCEPTS TO COMPILE:\n"
            for concept in chunk:
                name = concept["concept_name"]
                ctype = concept["concept_type"]
                existing_content = existing_pages.get(name, "")

                prompt += f"--- Concept: {name} (Type: {ctype}) ---\n"
                if existing_content:
                    prompt += f"EXISTING PAGE CONTENT:\n{existing_content}\n"
                else:
                    prompt += "NEW PAGE (No existing content)\n"
                prompt += "\n"

            try:
                response = self._generate(
                    model=self.model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=BatchCompileResponse,
                        max_output_tokens=65536,
                    ),
                )
                data = json.loads(response.text)
                all_updates.extend(BatchCompileResponse.model_validate(data).pages)
            except Exception as e:
                logger.error(f"Gemini batch_compile_pages error on chunk: {e}")
                if 'response' in locals() and hasattr(response, 'text'):
                    logger.error(f"Raw response length: {len(response.text)}")
                    logger.error(f"Raw response tail: {response.text[-500:]}")
                raise

        return all_updates

    def semantic_lint(self, index_md: str, pages_content: dict) -> List[LintIssue]:
        prompt = f"""Perform a semantic lint on the entire wiki.
Analyse the wiki holistically and return a list of semantic issues.

Issues to detect:
- Contradictions between pages
- Stale claims superseded by newer sources
- Orphan pages with no inbound links
- Important concepts mentioned but lacking their own page
- Missing cross-references between related pages
- Data gaps that could be filled

Also suggest new questions to investigate and new sources to look for
(use severity: "suggestion").

INDEX:
{index_md}

PAGES CONTENT:
"""
        for path, content in pages_content.items():
            prompt += f"\n--- Page: {path} ---\n{content}\n"

        try:
            response = self._generate(
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

    def merge_insight_into_page(
        self, existing_page_content: str, insight_summary: str, page_path: str
    ) -> str:
        prompt = f"""You are a knowledge curator. Merge the novel insight into the
existing wiki page naturally.

INSTRUCTIONS:
- Preserve ALL existing content and the YAML frontmatter exactly as-is.
- Add the insight as a new section or extend relevant sections naturally.
- Return the full updated page content as a complete markdown string
  (including the original frontmatter).

INSIGHT TO ADD:
{insight_summary}

EXISTING PAGE CONTENT:
{existing_page_content}
"""
        try:
            response = self._generate(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(),
            )
            return response.text
        except Exception as e:
            logger.error(f"Gemini merge_insight_into_page error: {e}")
            raise

    def repair_wiki(
        self,
        issues: List[LintIssue],
        pages_content: dict,
        valid_slugs: List[str],
    ) -> RepairResponseSchema:
        prompt = f"""You are a wiki repair agent. Fix all lint issues and return the
corrected pages.

{_SLUG_RULES_BLOCK}

ISSUES TO FIX:
{issues}

ALL CURRENT WIKI PAGES:
{pages_content}

VALID EXISTING SLUGS:
{valid_slugs}

REPAIR INSTRUCTIONS:

1. DUPLICATE PAGES — For every pair of duplicate / near-duplicate pages flagged:
   - Merge their content into one single comprehensive page.
   - Use the simpler canonical slug following the SLUG RULES above.
     Prefer "recurrent-neural-network" over "recurrent-neural-network-rnn" or
     "recurrent-neural-network-model-architecture".
   - Add the duplicate's path to pages_to_delete.
   - Update all wikilinks in other pages that referenced the deleted slug.

2. BROKEN WIKILINKS — For every broken wikilink:
   - Find the closest matching page from valid_slugs.
   - Update the wikilink to use the correct slug.
   - If no matching page exists, remove the brackets and leave plain text.

3. STALE CLAIMS — Update the relevant section with accurate information.
   Preserve all other content.

4. MISSING CROSS-REFERENCES — Add the appropriate [[wikilink]] in the
   relevant section of the page.

5. ORPHAN PAGES — Add appropriate [[wikilinks]] to the orphan page from
   related pages.

6. SUGGESTIONS (severity: suggestion) — implement only if straightforward:
   - Create new pages for clearly missing concepts.
   - Skip suggestions that require external research or web search.

RULES:
- Preserve all existing frontmatter fields. Only update content and wikilinks.
- Never delete a page unless it is a confirmed duplicate fully merged elsewhere.
- Always use [[wikilinks]] for internal references.
- Return ONLY pages that have actually changed, plus any new pages created.
- Do not return unchanged pages.
- pages_to_delete must only contain paths of duplicates whose content has been
  fully merged into another page.
"""
        try:
            response = self._generate(
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
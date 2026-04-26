import json
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


class QueryRoutingSchema(BaseModel):
    relevant_page_paths: List[str]


class QueryAnswerSchema(BaseModel):
    answer: str
    citations: List[Citation]
    insufficient_coverage: bool


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = settings.GEMINI_MODEL

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
    ) -> ChatResponse:
        system_instruction = (
            "You are a helpful knowledge assistant. Answer the user's question using ONLY the provided Wiki context.\n"
            "If the context does not contain the answer, say so clearly and set insufficient_coverage to true.\n"
            "Return your response in JSON format including citations to the used wiki pages.\n\n"
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
            return ChatResponse.model_validate(data)
        except Exception as e:
            logger.error(f"Gemini answer error: {e}")
            raise
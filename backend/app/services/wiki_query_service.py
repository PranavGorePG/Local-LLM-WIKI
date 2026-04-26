from app.schemas.chat import ChatRequest, ChatResponse
from app.services.gemini_service import GeminiService
from app.services.wiki_repository import WikiRepository
from app.core.logger import get_logger

logger = get_logger(__name__)

class WikiQueryService:
    def __init__(self, gemini: GeminiService, wiki_repo: WikiRepository):
        self.gemini = gemini
        self.wiki_repo = wiki_repo

    def handle_query(self, request: ChatRequest) -> ChatResponse:
        workspace_id = request.workspace_id
        
        if not request.history:
            raise ValueError("Empty chat history")
            
        last_query = request.history[-1].content
        
        # Load catalog
        pages = self.wiki_repo.list_pages(workspace_id)
        catalog = "\n".join(pages)
        
        if not pages:
            return ChatResponse(
                answer="The wiki is empty. Please ingest some documents first.",
                citations=[],
                insufficient_coverage=True
            )

        # Routing
        relevant_paths = self.gemini.route_query(last_query, catalog)
        
        # Gather context
        wiki_context = ""
        valid_paths = []
        for path in relevant_paths:
            try:
                metadata, content = self.wiki_repo.read_page(workspace_id, path)
                wiki_context += f"--- Page: {path} ---\nMetadata: {metadata}\n{content}\n\n"
                valid_paths.append(path)
            except FileNotFoundError:
                logger.warning(f"Routed to non-existent page: {path}")
                
        if not valid_paths:
            # Fallback to index or just fail
            return ChatResponse(
                answer="I could not find any relevant pages in the wiki to answer your question.",
                citations=[],
                insufficient_coverage=True
            )
            
        # Answer
        response = self.gemini.answer_query(request.history, wiki_context)
        return response

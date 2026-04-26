from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.wiki_query_service import WikiQueryService
from app.api.deps import get_wiki_query_service

router = APIRouter()

@router.post("", response_model=ChatResponse)
def chat_with_wiki(
    request: ChatRequest, 
    service: WikiQueryService = Depends(get_wiki_query_service)
):
    try:
        return service.handle_query(request)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

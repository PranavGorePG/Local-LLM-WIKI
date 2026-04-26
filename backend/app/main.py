from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes_workspaces, routes_documents, routes_wiki, routes_chat

app = FastAPI(title="LLM Wiki API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_workspaces.router, prefix="/api/workspaces", tags=["workspaces"])
app.include_router(routes_documents.router, prefix="/api/documents", tags=["documents"])
app.include_router(routes_wiki.router, prefix="/api/wiki", tags=["wiki"])
app.include_router(routes_chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/health")
def health_check():
    return {"status": "ok"}

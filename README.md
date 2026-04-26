# LLM Wiki Local

A local-only, pure LLM Wiki application that compiles your raw documents into an Obsidian-compatible Markdown vault using the Gemini API.

## Architecture

This application treats the LLM as a "compiler". Rather than dynamically searching raw documents on every chat query (RAG), it processes them once into a structured, highly-linked Markdown wiki. When you chat with the system, it strictly queries this generated wiki.

The stack consists of:
- **Frontend**: Streamlit
- **Backend**: FastAPI
- **Storage**: Local filesystem
- **LLM**: Gemini API

## Setup

1. **Install Python 3.10+**
2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**
   Copy `.env.example` to `.env` and set your Gemini API key:
   ```bash
   cp .env.example .env
   # Edit .env and insert your GEMINI_API_KEY
   ```

## Running the Application

1. **Start the FastAPI Backend**
   From the `llm_wiki_local` directory:
   ```bash
   python -m uvicorn backend.app.main:app --reload
   ```

2. **Start the Streamlit Frontend**
   In a new terminal, from the `llm_wiki_local` directory:
   ```bash
   python -m streamlit run frontend/Home.py
   ```

## Obsidian Integration

The generated workspaces are completely compatible with Obsidian. 
To view your knowledge graph and use backlinks:
1. Open Obsidian.
2. Select "Open folder as vault".
3. Navigate to `llm_wiki_local/workspaces/<your_workspace_id>/wiki` and select it.
4. Enjoy your generated wiki with full Graph View and `[[wikilink]]` support!

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
WORKSPACES_DIR = BASE_DIR / "workspaces"

RAW_DIR_NAME = "raw"
WIKI_DIR_NAME = "wiki"
OUTPUTS_DIR_NAME = "outputs"

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".md"}

WIKI_CATEGORIES = ["concepts", "entities", "topics", "sources"]

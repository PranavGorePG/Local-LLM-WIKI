import re

def generate_slug(text: str) -> str:
    """Generate a clean, stable slug for filenames and wikilinks."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text

def ensure_md_extension(filename: str) -> str:
    if not filename.endswith(".md"):
        return filename + ".md"
    return filename

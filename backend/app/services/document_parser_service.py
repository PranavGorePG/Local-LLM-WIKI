from pathlib import Path
import fitz  # PyMuPDF
from app.core.logger import get_logger

logger = get_logger(__name__)

class DocumentParserService:
    def parse_document(self, file_path: Path) -> str:
        ext = file_path.suffix.lower()
        if ext == ".pdf":
            return self._parse_pdf(file_path)
        elif ext in [".txt", ".md"]:
            return self._parse_text(file_path)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")

    def _parse_pdf(self, file_path: Path) -> str:
        text = []
        try:
            doc = fitz.open(file_path)
            for page in doc:
                text.append(page.get_text())
            doc.close()
        except Exception as e:
            logger.error(f"Error parsing PDF {file_path}: {e}")
            raise
        return "\n\n".join(text)

    def _parse_text(self, file_path: Path) -> str:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                return f.read()

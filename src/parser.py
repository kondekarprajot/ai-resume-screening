from __future__ import annotations

from pathlib import Path


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".doc", ".txt"}


class UnsupportedFileTypeError(ValueError):
    """Raised when a resume file type is not supported."""


def extract_text(file_path: str | Path) -> str:
    """Extract plain text from a PDF, DOC/DOCX, or TXT file."""
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileTypeError(f"Unsupported file type: {suffix}")

    if suffix == ".pdf":
        return _extract_pdf_text(path)
    if suffix == ".docx":
        return _extract_docx_text(path)
    if suffix == ".doc":
        return _extract_doc_text_with_tika(path)
    return path.read_text(encoding="utf-8", errors="ignore")


def _extract_pdf_text(path: Path) -> str:
    try:
        import pdfplumber

        with pdfplumber.open(path) as pdf:
            pages = [page.extract_text() or "" for page in pdf.pages]
        text = "\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

    try:
        import fitz

        with fitz.open(path) as document:
            return "\n".join(page.get_text() for page in document).strip()
    except Exception as exc:
        raise RuntimeError(f"Could not extract text from PDF: {path.name}") from exc


def _extract_docx_text(path: Path) -> str:
    try:
        from docx import Document
    except ImportError as exc:
        raise RuntimeError("python-docx is required to parse DOCX files.") from exc

    document = Document(path)
    paragraphs = [paragraph.text for paragraph in document.paragraphs]
    return "\n".join(paragraphs).strip()


def _extract_doc_text_with_tika(path: Path) -> str:
    try:
        from tika import parser
    except ImportError as exc:
        raise RuntimeError("Apache Tika is required to parse legacy DOC files.") from exc

    parsed = parser.from_file(str(path))
    return (parsed.get("content") or "").strip()

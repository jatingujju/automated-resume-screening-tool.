"""
extractor.py
------------
Phase 5: Resume text extraction.

Reads text from PDF, DOCX and TXT resumes.
Works with a file path OR an in-memory file (used by the Streamlit app / API).
"""

from io import BytesIO
from pathlib import Path

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def _extract_pdf(source) -> str:
    """Extract text from a PDF using pdfplumber (falls back to pypdf)."""
    text = ""
    try:
        import pdfplumber

        with pdfplumber.open(source) as pdf:
            pages = [(page.extract_text() or "") for page in pdf.pages]
        text = "\n".join(pages)
    except Exception:
        text = ""

    # Fallback: pypdf (the maintained successor of PyPDF2)
    if not text.strip():
        try:
            from pypdf import PdfReader

            if hasattr(source, "seek"):
                source.seek(0)
            reader = PdfReader(source)
            text = "\n".join((p.extract_text() or "") for p in reader.pages)
        except Exception:
            text = ""
    return text


def _extract_docx(source) -> str:
    """Extract text from a DOCX (paragraphs + table cells)."""
    from docx import Document

    doc = Document(source)
    parts = [p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                parts.append(cell.text)
    return "\n".join(parts)


def _extract_txt(source) -> str:
    if isinstance(source, (str, Path)):
        return Path(source).read_text(encoding="utf-8", errors="ignore")
    data = source.read()
    return data.decode("utf-8", errors="ignore") if isinstance(data, bytes) else data


def extract_text(source, filename: str = None) -> str:
    """
    Extract raw text from one resume.

    source   : file path (str/Path) or a file-like object (BytesIO / upload)
    filename : needed only when `source` is file-like (to know the extension)
    """
    name = filename or str(source)
    suffix = Path(name).suffix.lower()

    if suffix == ".pdf":
        return _extract_pdf(source)
    if suffix == ".docx":
        return _extract_docx(source)
    if suffix == ".txt":
        return _extract_txt(source)
    raise ValueError(f"Unsupported file type: {suffix}")


def load_resumes(folder: str) -> list:
    """
    Read every supported resume in `folder`.

    Returns a list of dicts: {"file_name": ..., "raw_text": ...}
    Unreadable / empty files are skipped with a warning
    (scanned PDFs need OCR, which this beginner project does not include).
    """
    resumes = []
    for path in sorted(Path(folder).iterdir()):
        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue
        try:
            text = extract_text(path)
        except Exception as exc:
            print(f"[WARN] Could not read {path.name}: {exc}")
            continue
        if not text.strip():
            print(f"[WARN] No text found in {path.name} (scanned PDF? needs OCR). Skipped.")
            continue
        resumes.append({"file_name": path.name, "raw_text": text})
    return resumes


def bytes_to_file(data: bytes) -> BytesIO:
    """Helper for uploads: wrap raw bytes so extract_text can read them."""
    return BytesIO(data)

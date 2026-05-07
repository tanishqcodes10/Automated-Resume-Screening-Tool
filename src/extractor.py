import os

def extract_text_from_txt(file_path: str) -> str:
    """Read plain text from a .txt file."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using pdfplumber (primary) and PyPDF2 (fallback)."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception:
        pass

    # Fallback: PyPDF2
    try:
        import PyPDF2
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text.strip()
    except Exception as e:
        print(f"  [!] Could not extract from PDF {file_path}: {e}")
        return ""

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        from docx import Document
        doc = Document(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        print(f"  [!] Could not extract from DOCX {file_path}: {e}")
        return ""

def extract_resume_text(file_path: str) -> str:
    """
    Auto-detect file type and extract text.
    Supports: .txt, .pdf, .docx
    """
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".txt":
        return extract_text_from_txt(file_path)
    elif ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        print(f"  [!] Unsupported file format: {ext}")
        return ""
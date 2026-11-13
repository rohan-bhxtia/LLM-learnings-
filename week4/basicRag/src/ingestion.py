
from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).parent.parent
PDF_PATH = BASE_DIR / "data" / "doc.pdf"

def extract_text():
    reader = PdfReader(PDF_PATH)
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    return full_text

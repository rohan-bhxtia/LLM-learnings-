from pathlib import Path
from pypdf import PdfReader

PDF_PATH = Path(__file__).parent / "msa.pdf"   # msa.pdf sits next to this script

reader = PdfReader(PDF_PATH)

print("total pages: ", len(reader.pages))

for page_number, page in enumerate(reader.pages, start=1):
    text = page.extract_text()


    print(f"\n=== Page {page_number} ===")
    print(text[:500] if text else " No text found")
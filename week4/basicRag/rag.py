from pathlib import Path
from pypdf import PdfReader

BASE_DIR = Path(__file__).parent
pdf_path = BASE_DIR / "data" / "doc.pdf"
reader = PdfReader(pdf_path)

 # we need entire text from pdf so that we can perform chunking
full_text = ""   
for page in reader.pages:
    text = page.extract_text()

    if text:
        full_text += text + "\n"

# chunking
chunk_size = 500
chunks = []

for i in range(0, len(full_text), chunk_size):
    chunk = full_text[i:i + chunk_size]
    chunks.append(chunk)

print(chunks)
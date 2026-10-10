from pathlib import Path
from pypdf import PdfReader

PDF_PATH = Path(__file__).parent / "msa.pdf"   # msa.pdf sits next to this script

reader = PdfReader(PDF_PATH)

print("total pages: ", len(reader.pages))

# for page_number, page in enumerate(reader.pages, start=1):
#     text = page.extract_text()


#     print(f"\n=== Page {page_number} ===")
#     print(text[:500] if text else " No text found")



# chunking
def chunk_text(text, size=500):
    chunks = []

    for start in range(0, len(text), size):
        chunk = text[start:start + size]
        chunks.append(chunk)

    return chunks    

sample_text = "A" * 1200
chunks = chunk_text(sample_text)

print("Number of chunks:", len(chunks))
print("First chunk length:", len(chunks[0]))
print("second chunk length:", len(chunks[1]))
print("Last chunk length:", len(chunks[2]))
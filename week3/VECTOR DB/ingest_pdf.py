from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader



# Configuration
PDF_PATH = Path(__file__).parent / "msa.pdf"
DB_PATH = Path(__file__).parent / "chroma_db"

COLLECTION = "contracts"
CHUNK_SIZE = 800
OVERLAP = 150
BATCH = 100


# Create or open the collection
def get_collection():
    client = chromadb.PersistentClient(path=str(DB_PATH))

    ef = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )

    collection = client.get_or_create_collection(
        name=COLLECTION,
        embedding_function=ef,
        metadata={"hnsw:space": "cosine"}
    )

    return collection


# Split text into overlapping chunks
def chunk_text(text, size=CHUNK_SIZE, overlap=OVERLAP):
    text = " ".join(text.split())

    chunks = []
    start = 0

    while start < len(text):
        chunk = text[start:start + size]
        chunks.append(chunk)
        start += size - overlap

    return chunks


# Read PDF, create records, and store them
def ingest(pdf_path):
    collection = get_collection()
    path = Path(pdf_path)

    ids = []
    documents = []
    metadatas = []

    reader = PdfReader(path)

    for page_no, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        chunks = chunk_text(text)

        for i, chunk in enumerate(chunks):
            ids.append(f"{path.stem}-p{page_no}-c{i}")

            documents.append(chunk)

            metadatas.append({
                "source": path.name,
                "page": page_no,
                "chunk": i
            })

    for b in range(0, len(ids), BATCH):
        collection.upsert(
            ids=ids[b:b + BATCH],
            documents=documents[b:b + BATCH],
            metadatas=metadatas[b:b + BATCH]
        )

    print(f"PDF: {path.name}")
    print(f"Chunks processed: {len(ids)}")
    print(f"Total records in collection: {collection.count()}")


# Run the ingestion
if __name__ == "__main__":
    ingest(PDF_PATH)


# this can show which models are supported by chroma DB
from chromadb.utils import embedding_functions
print(dir(embedding_functions))

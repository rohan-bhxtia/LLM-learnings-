import chromadb
from pathlib import Path

# Get the project root directory
BASE_DIR = Path(__file__).parent.parent

# Create a persistent ChromaDB client
DB_PATH = BASE_DIR / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))


#making a collection
collection = client.get_or_create_collection(
    name="documents",
    metadata={"hnsw:space": "cosine"}
)

def store_chunks(chunks, embeddings):

    ids = []
    for i in range(len(chunks)):
        ids.append(str(i))

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )
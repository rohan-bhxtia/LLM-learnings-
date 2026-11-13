from src.vector_store import collection
from src.embeddings import create_embeddings

def retrieve_chunks(query):
    
    query_embedding = create_embeddings([query])

    # Search ChromaDB
    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=3
    )

    return results["documents"][0]
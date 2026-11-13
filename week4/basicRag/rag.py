
from src.ingestion import extract_text
from src.chunking import chunk_text
from src.embeddings import create_embeddings
from src.vector_store import store_chunks, collection
from src.retrieval import retrieve_chunks
from src.generation import generate_answer


# Check whether the collection already contains documents
existing_data = collection.count()

if existing_data == 0:
    print("Ingesting PDF...")

    full_text = extract_text()
    chunks = chunk_text(full_text)
    embeddings = create_embeddings(chunks)

    store_chunks(chunks, embeddings)

    print("Total chunks:", len(chunks))
    print("Total embeddings:", len(embeddings))
    print("Vector dimensions:", len(embeddings[0]))
    print("Chunks successfully stored in ChromaDB!")

else:
    print(f"ChromaDB already contains {existing_data} chunks.")


# Question-answering loop
while True:
    query = input("\nAsk your question (or type 'quit'): ")

    if query.lower() == "quit":
        print("Exiting RAG system...")
        break

    relevant_chunks = retrieve_chunks(query)

    context = "\n\n".join(relevant_chunks)

    answer = generate_answer(query, context)

    print("\nAnswer:", answer)

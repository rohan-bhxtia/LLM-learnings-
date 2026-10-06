from sentence_transformers import SentenceTransformer
from cosine import cosine

model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(docs,query,top_k):
    results = []
    doc_vectors = []
    for doc in docs:
        vector = model.encode(doc)
        doc_vectors.append(vector)

    query_vector = model.encode(query)    



    for doc,vector in zip(docs, doc_vectors):
        score = cosine(query_vector,vector)
        results.append((score,doc))

    results.sort(reverse=True)


    return results[:top_k]
## end
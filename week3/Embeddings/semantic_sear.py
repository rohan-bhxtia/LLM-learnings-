from sentence_transformers import SentenceTransformer
import numpy as np
from cosine import cosine

model = SentenceTransformer("all-MiniLM-L6-v2")

docs = [
    "The supplier may terminate this agreement with 30 days written notice.",
    "All invoices must be paid within 45 days of receipt.",
    "Employees can work remotely two days per week.",
    "Confidential information must not be disclosed to third parties.",
]

query = "How can the vendor exit the contract?"

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
top_k = 2

for score, doc in results[:top_k]:
      print(score,doc)

# Week 3 — Embeddings

Learning **embeddings**, comparing them with **cosine similarity**, and using them to build a small **semantic search**.

---

## Files in this folder

| File | What it does |
|---|---|
| [cosine.py](cosine.py) | Defines `cosine(a, b)`, a cosine similarity function used by the other scripts. |
| [embeddings.py](embeddings.py) | Turns two sentences into embeddings and measures how similar they are. |
| [semantic_search.py](semantic_search.py) | Searches a list of contract clauses by **meaning** and returns the top matches for a question. |

### Setup

```bash
pip install numpy sentence-transformers
```

Run the scripts from inside this folder so that `from cosine import cosine` works:

```bash
cd week3/Embeddings
python embeddings.py
python semantic_search.py
```

The first run downloads the `all-MiniLM-L6-v2` model (~90 MB) from Hugging Face. You may see `Warning: You are sending unauthenticated requests to the HF Hub`. It's harmless; setting an `HF_TOKEN` environment variable removes it.

---

## 1. What is an embedding?

An **embedding** is a list of numbers (a vector) that represents the *meaning* of something: a word, a sentence, an image, or a document.

```
"cat"    -> [0.21, -0.43, 0.88, ..., 0.05]
"kitten" -> [0.19, -0.40, 0.91, ..., 0.07]
"car"    -> [-0.72, 0.15, 0.02, ..., 0.64]
```

The model is trained so that **texts with similar meanings get vectors that point in similar directions**. `cat` and `kitten` end up close together; `car` ends up far away.

| Property | Meaning |
|---|---|
| **Dimension** | How many numbers are in each vector. `all-MiniLM-L6-v2` gives **384**. |
| **Dense** | Almost every value is non-zero, unlike bag-of-words vectors. |
| **Semantic** | Distance between vectors reflects difference in meaning. |
| **Fixed size** | A 3-word sentence and a long paragraph both become 384 numbers. |

---

## 2. Cosine similarity — [cosine.py](cosine.py)

```python
import numpy as np

def cosine(a, b):
    similarity = np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
    return similarity
```

Formula: `cos(a, b) = (a · b) / (‖a‖ × ‖b‖)`

It measures the **angle** between two vectors and ignores their length:

| Score | Meaning |
|---|---|
| **1** | Same direction (very similar) |
| **0** | Perpendicular (unrelated) |
| **-1** | Opposite direction |

### Worked example

For `a = [1, 2, 3]` and `b = [4, 5, 6]`:

1. Dot product: `1·4 + 2·5 + 3·6 = 32`
2. `‖a‖ = √14 ≈ 3.742`
3. `‖b‖ = √77 ≈ 8.775`
4. `32 / (3.742 × 8.775) ≈ 0.9746`

```python
from cosine import cosine
cosine([1, 2, 3], [4, 5, 6])   # 0.9746
cosine([1, 0], [0, 1])         # 0.0   (perpendicular)
cosine([1, 2], [-1, -2])       # -1.0  (opposite)
```

### Other similarity measures

| Metric | Formula | Higher means |
|---|---|---|
| Cosine similarity | `(a · b) / (‖a‖ · ‖b‖)` | more similar |
| Dot product | `a · b` | more similar |
| Euclidean distance | `‖a − b‖` | *less* similar |

> If vectors are **normalized** (length 1), cosine similarity equals the dot product, which is faster to compute.

---

## 3. Comparing two sentences — [embeddings.py](embeddings.py)

```python
model = SentenceTransformer("all-MiniLM-L6-v2")

text1 = " python is a programming language"
text2 = " there is a programming language called python "

vector1 = model.encode(text1)
vector2 = model.encode(text2)

similarity = cosine(vector1, vector2)
```

Output:

```
similarity:  0.89287615
```

The sentences are worded differently but mean nearly the same thing, so the score is high.

> **Common mistake:** `cosine(text1, text2)` fails with
> `ufunc 'multiply' did not contain a loop with signature matching types (dtype('<U47'), ...)`.
> That error means NumPy was given **strings** instead of numbers. Always compare the **vectors** returned by `model.encode`, not the original text.

---

## 4. Semantic search — [semantic_search.py](semantic_search.py)

This script finds the contract clauses most relevant to a question, even when they share no keywords with it.

**How it works:**

1. Embed every document in `docs`.
2. Embed the `query`.
3. Score each document with `cosine(query_vector, doc_vector)`.
4. Sort by score (highest first) and print the top `k` (here `top_k = 2`).

```
Documents ──► model.encode ──► doc vectors ─┐
                                            ├──► cosine scores ──► sort ──► top k
Query ──────► model.encode ──► query vector ┘
```

Query: `"How can the vendor exit the contract?"`

Output:

```
0.5370795 The supplier may terminate this agreement with 30 days written notice.
0.21327396 All invoices must be paid within 45 days of receipt.
```

The top result contains none of the words *vendor*, *exit*, or *contract*, yet it's clearly the right answer. The model understands that **vendor ≈ supplier**, **exit ≈ terminate**, and **contract ≈ agreement**. A plain keyword search would have missed it.

Notice also the large gap between the first and second scores (0.54 vs 0.21). That's a sign the top match is a confident one.

### Ideas to improve it

- **Encode all documents in one call:** `model.encode(docs)` is faster than a loop.
- **Normalize vectors:** `model.encode(docs, normalize_embeddings=True)` lets you use `np.dot` instead of full cosine.
- **Add a score threshold** so unrelated questions return "no good match" instead of the closest bad match.
- **Use a vector database** (FAISS, Chroma, Qdrant, pgvector) once you have thousands of documents.

---

## 5. Where this leads: RAG

Semantic search is the **retrieval** half of **RAG (Retrieval-Augmented Generation)**:

```
Documents ──► split into chunks ──► embed ──► store in vector DB
                                                     │
User question ──► embed ──► find top-k most similar ◄┘
                                     │
                                     ▼
                     send question + chunks to an LLM ──► answer
```

[semantic_search.py](semantic_search.py) already does everything up to "find top-k". The next step is to pass those top chunks to an LLM as context.

Other uses of embeddings: recommendations, clustering similar texts, finding near-duplicates, and as input features for classifiers.

---

## 6. Gotchas

- **Use the same model** for documents and queries. Vectors from different models can't be compared.
- **Pass vectors, not strings**, to `cosine`.
- **Zero vectors** make `cosine` divide by zero and return `nan`.
- **Chunk long text.** Models have an input length limit and truncate anything beyond it.
- **Scores are relative.** A "good" score differs between models, so compare results by rank rather than a fixed number.

---

## 7. Next steps

- [x] Write a cosine similarity function
- [x] Generate real sentence embeddings
- [x] Build a basic semantic search
- [ ] Batch-encode documents and normalize vectors
- [ ] Add a minimum-score threshold
- [ ] Store vectors in FAISS or Chroma
- [ ] Send the top results to an LLM to build a mini RAG app

---

## References

- [Sentence-Transformers documentation](https://www.sbert.net/)
- [all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [NumPy `dot`](https://numpy.org/doc/stable/reference/generated/numpy.dot.html) · [NumPy `linalg.norm`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html)
- [Cosine similarity (Wikipedia)](https://en.wikipedia.org/wiki/Cosine_similarity)

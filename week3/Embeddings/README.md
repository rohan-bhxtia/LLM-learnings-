# Week 3 — Embeddings

Notes and code for learning **embeddings** and how to compare them with **cosine similarity**.

---

## 1. What is an embedding?

An **embedding** is a list of numbers (a vector) that represents the *meaning* of something: a word, a sentence, an image, or a whole document.

```
"cat"    -> [0.21, -0.43, 0.88, ..., 0.05]   (e.g. 384 / 768 / 1536 numbers)
"kitten" -> [0.19, -0.40, 0.91, ..., 0.07]
"car"    -> [-0.72, 0.15, 0.02, ..., 0.64]
```

The model is trained so that **things with similar meanings get vectors that point in similar directions**. In the example above, `cat` and `kitten` are close together and `car` is far away.

Computers can't compare meaning directly, but they can compare numbers. Embeddings turn "how similar are these two texts?" into a math problem.

### Key properties

| Property | Meaning |
|---|---|
| **Dimension** | How many numbers are in each vector (e.g. 384, 768, 1536, 3072). |
| **Dense** | Almost every value is non-zero, unlike one-hot / bag-of-words vectors. |
| **Semantic** | Distance in the vector space reflects difference in meaning. |
| **Fixed size** | A 3-word sentence and a 300-word paragraph both become vectors of the same length. |

---

## 2. Measuring similarity

Once you have two vectors, you need a way to score how close they are. The three common choices:

| Metric | Formula | Range | Higher means |
|---|---|---|---|
| **Cosine similarity** | `(a · b) / (‖a‖ · ‖b‖)` | -1 to 1 | more similar |
| **Dot product** | `a · b` | unbounded | more similar |
| **Euclidean distance** | `‖a − b‖` | 0 to ∞ | *less* similar |

**Cosine similarity** is the default for text embeddings because it only cares about the **direction** of the vectors, not their length. A long document and a short sentence on the same topic can still score high.

How to read a cosine score:

- **1** → same direction (very similar)
- **0** → perpendicular (unrelated)
- **-1** → opposite direction

> Tip: if your vectors are already **normalized** (length 1), cosine similarity and dot product give the same result. Many embedding APIs return normalized vectors, so a plain dot product is enough and is faster.

---

## 3. The code: [embeddings.py](embeddings.py)

```python
import numpy as np

a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

similarity = np.dot(a, b) / (
    np.linalg.norm(a) * np.linalg.norm(b)
)
print(similarity)
```

This computes cosine similarity between two small vectors by hand.

### Step by step

1. **Dot product**: `a · b = 1·4 + 2·5 + 3·6 = 32`
2. **Length of a**: `‖a‖ = √(1² + 2² + 3²) = √14 ≈ 3.742`
3. **Length of b**: `‖b‖ = √(4² + 5² + 6²) = √77 ≈ 8.775`
4. **Cosine similarity**: `32 / (3.742 × 8.775) ≈ 0.9746`

### Run it

```bash
pip install numpy
python embeddings.py
```

Expected output:

```
0.9746318461970762
```

A score of **~0.97** means the two vectors point in almost the same direction. Both increase from first to last element, so they are "similar".

---

## 4. From toy vectors to real embeddings

The script uses hand-written 3-number vectors. In practice an **embedding model** produces the vectors for you. Example with the open-source `sentence-transformers` library (runs locally, no API key):

```python
# pip install sentence-transformers
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")   # 384-dim vectors

sentences = [
    "I love playing with my cat",
    "My kitten is very playful",
    "The stock market crashed today",
]
vectors = model.encode(sentences, normalize_embeddings=True)

def cosine(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(cosine(vectors[0], vectors[1]))  # high  -> similar meaning
print(cosine(vectors[0], vectors[2]))  # low   -> unrelated
```

The two cat sentences share almost no words, but they still score high because the model captures **meaning**, not just matching words.

---

## 5. Where embeddings are used

- **Semantic search**: find documents by meaning, not exact keywords.
- **RAG (Retrieval-Augmented Generation)**: embed your documents, retrieve the most similar chunks for a question, and give them to an LLM as context.
- **Recommendations**: "users who liked this also liked…"
- **Clustering**: group similar support tickets, reviews, or articles.
- **Deduplication**: spot near-duplicate text.
- **Classification**: use embeddings as input features for a simple classifier.

### Typical RAG / semantic search flow

```
Documents ──► split into chunks ──► embed ──► store in vector DB
                                                     │
User question ──► embed ──► find top-k most similar ◄┘
                                     │
                                     ▼
                     send question + chunks to the LLM ──► answer
```

Common vector stores: **FAISS**, **Chroma**, **Pinecone**, **Qdrant**, **Weaviate**, **pgvector** (Postgres).

---

## 6. Gotchas

- **Use the same model** for your documents and your queries. Vectors from different models live in different spaces and can't be compared.
- **Normalize** if you plan to use dot product as the similarity score.
- **Chunk long text.** Models have an input limit; very long inputs get truncated or lose detail.
- **Scores are relative.** "0.8" doesn't mean the same thing across models. Rank results instead of relying on a fixed threshold.
- **Zero vectors** make cosine similarity divide by zero, so guard against them.

---

## 7. Next steps

- [ ] Write a `cosine_similarity(a, b)` function and test it with different vectors (identical, opposite, perpendicular).
- [ ] Generate real embeddings with `sentence-transformers` and compare sentences.
- [ ] Build a tiny semantic search: embed ~20 sentences, embed a query, return the top 3 matches.
- [ ] Store the vectors in FAISS or Chroma.
- [ ] Combine retrieval with an LLM to build a mini RAG app.

---

## References

- [NumPy `dot`](https://numpy.org/doc/stable/reference/generated/numpy.dot.html) · [NumPy `linalg.norm`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html)
- [Sentence-Transformers documentation](https://www.sbert.net/)
- [Cosine similarity (Wikipedia)](https://en.wikipedia.org/wiki/Cosine_similarity)

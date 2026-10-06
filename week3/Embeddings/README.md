# Week 3 — Embeddings

Learning **embeddings**, comparing them with **cosine similarity**, and building an interactive **semantic search** over contract clauses.

---

## Files in this folder

| File | What it does | Run it? |
|---|---|---|
| [cosine.py](cosine.py) | `cosine(a, b)`: cosine similarity between two vectors. | No, it's imported by the others |
| [emb_learning.py](emb_learning.py) | Embeds two sentences and prints how similar they are. | `python emb_learning.py` |
| [semantic_search.py](semantic_search.py) | Loads the model and defines `semantic_search()`, which ranks documents against a query. | No, it's imported by `test_run.py` |
| [test_run.py](test_run.py) | Interactive search: ask questions about a contract and get the most relevant clause. | `python test_run.py` |
| [requirements.txt](requirements.txt) | Pinned dependencies. | |

```
cosine.py ◄──── emb_learning.py
    ▲
    └────────── semantic_search.py ◄──── test_run.py
                (loads the model)        (docs + question loop)
```

### Setup

```bash
pip install -r requirements.txt
cd week3/Embeddings          # run from here so `from cosine import cosine` works
python emb_learning.py
python test_run.py
```

[requirements.txt](requirements.txt) pins `numpy` and `sentence-transformers` (which pulls in `torch` and `transformers`).

The first run downloads the `all-MiniLM-L6-v2` model (~90 MB). You may see `Warning: You are sending unauthenticated requests to the HF Hub`. It's harmless; setting an `HF_TOKEN` environment variable removes it.

---

## 1. What is an embedding?

An **embedding** is a list of numbers (a vector) that represents the *meaning* of a piece of text.

```
"cat"    -> [0.21, -0.43, 0.88, ..., 0.05]
"kitten" -> [0.19, -0.40, 0.91, ..., 0.07]
"car"    -> [-0.72, 0.15, 0.02, ..., 0.64]
```

The model is trained so that **texts with similar meanings get vectors pointing in similar directions**. `cat` and `kitten` end up close; `car` ends up far away.

| Property | Meaning |
|---|---|
| **Dimension** | Numbers per vector. `all-MiniLM-L6-v2` gives **384**. |
| **Dense** | Almost every value is non-zero. |
| **Semantic** | Distance between vectors reflects difference in meaning. |
| **Fixed size** | A 3-word sentence and a whole paragraph both become 384 numbers. |

---

## 2. Cosine similarity — [cosine.py](cosine.py)

```python
def cosine(a, b):
    similarity = np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )
    return similarity
```

`cos(a, b) = (a · b) / (‖a‖ × ‖b‖)` measures the **angle** between two vectors and ignores their length.

| Score | Meaning |
|---|---|
| **1** | Same direction (very similar) |
| **0** | Perpendicular (unrelated) |
| **-1** | Opposite direction |

Worked example for `a = [1, 2, 3]`, `b = [4, 5, 6]`:

1. `a · b = 1·4 + 2·5 + 3·6 = 32`
2. `‖a‖ = √14 ≈ 3.742`, `‖b‖ = √77 ≈ 8.775`
3. `32 / (3.742 × 8.775) ≈ 0.9746`

> If vectors are **normalized** (length 1), cosine similarity equals the plain dot product.

---

## 3. Comparing two sentences — [emb_learning.py](emb_learning.py)

```python
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

---

## 4. Semantic search — [semantic_search.py](semantic_search.py) + [test_run.py](test_run.py)

### How it works

```
          ONCE, at startup                       FOR EVERY QUESTION
┌───────────────────────────────┐    ┌──────────────────────────────────────┐
│ docs ──► model.encode(docs)   │    │ question ──► model.encode(question)  │
│          = doc_vectors        │──► │ cosine(question_vector, each doc)    │
└───────────────────────────────┘    │ sort by score ──► return top_k       │
                                     └──────────────────────────────────────┘
```

1. [test_run.py](test_run.py) holds 8 contract clauses in `docs`.
2. It encodes **all of them once** in a single batch: `doc_vectors = model.encode(docs)`.
3. In a loop, it reads a question and calls `semantic_search(docs, doc_vectors, query, 1)`.
4. `semantic_search()` encodes **only the question**, scores it against every stored document vector, sorts the scores and returns the best `top_k`.
5. Type `stop` (any capitalization) to quit. An empty line just asks again.

**Why encode the documents once?** Encoding is the slow step. With the documents encoded up front, each question costs a single `encode` call, no matter how many documents there are.

**Why import `model` from `semantic_search.py`?** Both files then share one loaded model, instead of loading the same ~90 MB model twice.

### Example session

```
Ask your question (type 'stop' to quit): how can the vendor exit the contract?

Score: 0.590
The supplier may terminate this agreement by providing the customer with at least 30 days written notice.
...
```

| Question | Top clause | Score |
|---|---|---|
| how can the vendor exit the contract? | Termination ("The supplier may terminate…") | 0.590 |
| when do invoices need to be paid? | Payment ("All invoices… within 45 days") | 0.729 |
| can staff work from home? | Remote work ("Employees… may work remotely…") | 0.540 |
| what happens if the supplier leaks our data? | Confidentiality ("must not be disclosed…") | 0.587 |

None of these questions repeat the clause's wording: *vendor/supplier*, *exit/terminate*, *staff/employees*, *work from home/remotely*, *leaks/disclosed*. The model matches on **meaning**, which plain keyword search can't do.

---

## 5. Errors hit while building this (and what they mean)

| Error | Cause | Fix |
|---|---|---|
| `ufunc 'multiply' did not contain a loop with signature matching types (dtype('<U47'), ...)` | Passed **text** to `cosine()`. `<U47` is NumPy's name for a string. | Pass the vectors from `model.encode(...)`. |
| `ValueError: Modality 'audio' is not supported by this SentenceTransformer model` | Passed **vectors** where `model.encode()` expected **text**, so the model mistook the number arrays for audio. | Encode the text once and give the function the vectors separately. |
| `NameError: name 'stop' is not defined` | `query == stop` without quotes made Python look for a variable called `stop`. | Compare with the string `"stop"`. |
| `SyntaxError` on a line ending in `/` | A line can't end mid-expression unless it's inside brackets. | Wrap the expression in `( ... )`. |

---

## 6. Gotchas

- **Use the same model** for documents and queries. Vectors from different models can't be compared.
- **Zero vectors** make `cosine` divide by zero and return `nan`.
- **Long text gets truncated.** Models have an input limit, so split long documents into chunks.
- **Scores are relative.** Compare results by rank; what counts as a "good" score differs between models.
- **Re-encode `doc_vectors` whenever `docs` changes**, or results will point at the wrong text.

---

## 7. Where this leads: RAG

Semantic search is the **retrieval** step of **RAG (Retrieval-Augmented Generation)**:

```
Documents ──► chunk ──► embed ──► store
                                    │
Question ──► embed ──► top-k match ◄┘ ──► question + top chunks ──► LLM ──► answer
```

[test_run.py](test_run.py) already does everything up to "top-k match". The next step is sending those clauses to an LLM so it can write the answer in its own words.

---

## 8. Progress

- [x] Write a cosine similarity function
- [x] Generate sentence embeddings
- [x] Build semantic search
- [x] Batch-encode documents once and reuse the vectors
- [x] Interactive question loop
- [ ] Return the top 3 results instead of 1
- [ ] Add a minimum-score threshold ("no good match found")
- [ ] Store vectors in FAISS or Chroma
- [ ] Send the top results to an LLM to build a mini RAG app

---

## References

- [Sentence-Transformers documentation](https://www.sbert.net/)
- [all-MiniLM-L6-v2 model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)
- [NumPy `dot`](https://numpy.org/doc/stable/reference/generated/numpy.dot.html) · [NumPy `linalg.norm`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.norm.html)
- [Cosine similarity (Wikipedia)](https://en.wikipedia.org/wiki/Cosine_similarity)

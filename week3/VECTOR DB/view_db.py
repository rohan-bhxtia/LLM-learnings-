import csv
import sys
from pathlib import Path
import chromadb

DB_PATH = Path(__file__).parent / "chroma_db"

client = chromadb.PersistentClient(path=str(DB_PATH))

# Show every collection in the database
print("========== COLLECTIONS ==========")
for col in client.list_collections():
    print(f"{col.name}: {col.count()} records | settings: {col.metadata}")

collection = client.get_collection("contracts")

# Fetch everything, including one embedding so we can see what a vector looks like
data = collection.get(include=["documents", "metadatas", "embeddings"])

records = sorted(
    zip(data["ids"], data["documents"], data["metadatas"], data["embeddings"]),
    key=lambda r: (r[2]["page"], r[2]["chunk"]),
)

print("\n========== RECORDS ==========")
for doc_id, doc, meta, _ in records:
    print(f"\n[{doc_id}]  page {meta['page']}, chunk {meta['chunk']}  ({len(doc)} chars)")
    print(f"  {doc[:150]}...")

first_id, _, _, first_vector = records[0]
print("\n========== WHAT A VECTOR LOOKS LIKE ==========")
print(f"{first_id}: {len(first_vector)} numbers")
print(f"first 8: {[round(float(x), 4) for x in first_vector[:8]]}")

# Optional: save everything to a CSV you can open in VS Code or Excel
# usage: python view_db.py export.csv
if len(sys.argv) > 1:
    out = Path(sys.argv[1])
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "source", "page", "chunk", "document"])
        for doc_id, doc, meta, _ in records:
            writer.writerow([doc_id, meta["source"], meta["page"], meta["chunk"], doc])
    print(f"\nSaved {len(records)} records to {out}")


import chromadb

client = chromadb.Client()

first_dataBox = client.get_or_create_collection(
    name="clause",
    metadata={"hnsw:space": "cosine"}
)

# ADD
first_dataBox.add(
    ids=["clause1", "clause2", "clause3"],
    documents=[
        "The supplier may terminate the contract with 30 days notice.",
        "All invoices must be paid within 45 days.",
        "Confidential information must not be shared."
    ]
)

print("Clauses stored:", first_dataBox.count())


# QUERY
query = "how can the vendor exit the contract?"

output = first_dataBox.query(
    query_texts=[query],
    n_results=2,
    include=["documents", "distances"]
)

print("\n========== QUERY ==========")
print("Question:", query)

for i in range(len(output["documents"][0])):
    doc = output["documents"][0][i]
    distance = output["distances"][0][i]

    print("\nDocument:", doc)
    print("Similarity:", round(1 - distance, 3))
    print("Distance:", round(distance, 3))


# GET
get_ids = ["clause2"]

result = first_dataBox.get(ids=get_ids)

print("\n========== GET ==========")
print("Requested IDs:", get_ids)

for i in range(len(result["ids"])):
    print("ID:", result["ids"][i])
    print("Document:", result["documents"][i])


# DELETE
delete_ids = ["clause2"]

count_before = first_dataBox.count()

first_dataBox.delete(ids=delete_ids)

print("\n========== DELETE ==========")
print("Deleted IDs:", delete_ids)
print("Clauses:", count_before, "->", first_dataBox.count())

result = first_dataBox.get()

print("Remaining IDs:", result["ids"])

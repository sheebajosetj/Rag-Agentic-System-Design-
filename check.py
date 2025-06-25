import chromadb

client = chromadb.PersistentClient(path="./db")
collection = client.get_or_create_collection("federal_docs")

print("✅ Connected to ChromaDB")
print("📦 Total documents in collection:", collection.count())

results = collection.get(include=['documents'])

for i, doc in enumerate(results["documents"]):
    print(f"\nDoc {i+1}:\n{doc[:300]}\n{'-'*40}")

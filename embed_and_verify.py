import psycopg2
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction
import os
from dotenv import load_dotenv  # ✅ Add this
load_dotenv()  # ✅ Load .env

# --- 1. Connect to PostgreSQL ---
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)

cursor = conn.cursor()
cursor.execute("SELECT title, summary FROM federal_docs WHERE summary IS NOT NULL AND summary != 'No summary available';")
rows = cursor.fetchall()

print(f"📥 Retrieved {len(rows)} rows from PostgreSQL.")

if not rows:
    print("❌ No documents found.")
    exit()

# --- 2. Prepare documents ---
documents = [f"{title}\n\n{summary}" for title, summary in rows]

# --- 3. Generate embeddings ---
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents, show_progress_bar=True)

chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_or_create_collection("federal_docs")

# --- 5. Add documents to Chroma ---
for i, text in enumerate(documents):
    collection.add(
        documents=[text],
        ids=[f"doc_{i}"],
        embeddings=[embeddings[i]]
    )

print(f"✅ Inserted {collection.count()} documents into ChromaDB.")

# --- 6. Query test ---
query = "What did the FDA announce?"
results = collection.query(query_texts=[query], n_results=3)

print("🔍 Query Results:")
for doc in results['documents'][0]:
    print("-", doc[:200])  # print first 200 chars of each result

# --- 7. Clean up ---
cursor.close()
conn.close()

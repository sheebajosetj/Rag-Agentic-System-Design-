# embed_into_chroma.py

import psycopg2
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import os
from dotenv import load_dotenv

load_dotenv()

# --- 1. PostgreSQL CONNECTION ---
conn = psycopg2.connect(
    dbname=os.getenv("POSTGRES_DB"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("POSTGRES_HOST"),
    port=os.getenv("POSTGRES_PORT")
)

cursor = conn.cursor()
cursor.execute("""
    SELECT title, summary FROM federal_documents 
    WHERE summary IS NOT NULL AND summary != 'No summary available'
""")
rows = cursor.fetchall()

if not rows:
    print("No documents found to embed.")
    exit()

# --- 2. Prepare documents for embedding ---
docs = []
for title, summary in rows:
    content = f"{title}\n\n{summary}"
    docs.append(Document(page_content=content))

# --- 3. Create ChromaDB client ---
embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectordb = Chroma(persist_directory="chroma_db", embedding_function=embedding_function)

# --- 4. Embed documents ---
vectordb.add_documents(docs)
vectordb.persist()

print(f"✅ Embedded and stored {len(docs)} documents in ChromaDB.")

# Cleanup
cursor.close()
conn.close()

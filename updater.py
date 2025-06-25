
# fetch_data/updater.py
import asyncio
from datetime import date
from downloader import fetch_documents
from processor import process_documents, Document
import asyncpg

DB_CONFIG = {
    "user": "postgres",
    "password": "5080",
    "database": "fd_data",
    "host": "localhost",
    "port": 5432 
}

TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS federal_docs (
    id SERIAL PRIMARY KEY,
    title TEXT,
    publication_date DATE,
    executive_order_number TEXT,
    summary TEXT
);
"""

async def insert_documents(conn, docs: list[Document]):
    await conn.execute(TABLE_SCHEMA)
    for doc in docs:
        await conn.execute("""
    INSERT INTO federal_docs 
    (title, publication_date, executive_order_number, summary)
    VALUES ($1, $2, $3, $4)
""",
    doc.title,
    doc.publication_date,
    doc.executive_order_number,
    doc.summary
)


async def run_pipeline():
    today = date.today()
    start = today.replace(day=max(1, today.day - 7)).strftime("%Y-%m-%d")
    end = today.strftime("%Y-%m-%d")

    

    print(f"Fetching documents from {start} to {end}")
    raw_docs = await fetch_documents(start, end)
   
    print("Sample raw_doc:")
    print(raw_docs[0])  # This helps us see what keys are present

    docs = process_documents(raw_docs)


    pool = await asyncpg.create_pool(**DB_CONFIG)
    async with pool.acquire() as conn:
        await insert_documents(conn, docs)
    print(f"Inserted {len(docs)} documents.")

if __name__ == "__main__":
    asyncio.run(run_pipeline())

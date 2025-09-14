# Agentic RAG - AI  

---

## 📌 Overview  
This project implements an **Agentic Retrieval-Augmented Generation (RAG) system** for working with U.S. Federal Register data. It fetches documents asynchronously, processes them into structured formats, stores them in ChromaDB, and enables natural language querying using **Gemini**.  

---

## ⚙️ Setup  

### 1. Clone Repository  
```bash
git clone https://github.com/yourusername/agentic-rag-ai.git
cd agentic-rag-ai


2. Create & Activate Environment

If you already have a Conda environment set up:

.\env\Scripts\activate

3. Install Requirements

Modules
downloader.py

Fetches Federal Register documents asynchronously using aiohttp.

Accepts a start & end date range, retrieves document metadata & HTTPS content.

Libraries used: aiohttp, typing.List.

Note: Asynchronous HTTP requests prevent blocking during API fetch.

processor.py

Converts raw document data (dicts) into structured Document objects using Pydantic.

Handles missing fields with defaults & ensures correct date formatting.

Libraries used: pydantic.

updater.py

Periodically fetches daily updates from the Federal Register API.

Inserts/syncs updates into PostgreSQL + ChromaDB.

Libraries used: asyncio, datetime, asyncpg.

query_utils.py

Searches relevant documents from ChromaDB using semantic embeddings.

Builds a context-aware prompt for Gemini LLM.

Returns a generated answer based on retrieved context.

🚨 Known Issues

LangChain deprecation warnings

Since LangChain v0.2.x, integrations like Chroma & HuggingFace have moved to external packages.

Fix: Install updated integration packages

pip install -U langchain langchain-community langchain-chroma langchain-huggingface


Database Integration

PostgreSQL is connected to ChromaDB for persistent storage.

Retrieved results are displayed via the HTML frontend.



from chroma_client import vectordb
from gemini_client import ask_gemini

def answer_query(query: str) -> str:
    docs = vectordb.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"""Answer the following question using the context below:
    
    Context:
    {context}

    Question: {query}
    """
    return ask_gemini(prompt)

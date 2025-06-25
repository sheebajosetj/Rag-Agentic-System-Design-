from flask import Flask, render_template, request
import os
import chromadb
from google.generativeai import GenerativeModel
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# --- Load ChromaDB ---
chroma_client = chromadb.PersistentClient(path="./db")
collection = chroma_client.get_or_create_collection("federal_docs")


# --- Setup Gemini ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
model = GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form["question"]

    # Step 1: Query Chroma
    results = collection.query(query_texts=[question], n_results=3)
    retrieved_docs = results["documents"][0]

    # 🔍 Print retrieved documents
    print("📄 Retrieved docs from Chroma:")
    for i, doc in enumerate(retrieved_docs):
        print(f"Doc {i+1}:\n{doc[:300]}\n---\n")  # show first 300 characters

    # Step 2: Build prompt for Gemini
    context = "\n\n".join(retrieved_docs)
    prompt = f"Use the following FDA documents to answer the question:\n\n{context}\n\nQuestion: {question}"

    print("\n===== PROMPT SENT TO GEMINI =====")
    print(prompt[:1000])  # You can print full if needed
    print("===== END OF PROMPT =====\n")



    # Step 3: Get response from Gemini
    response = model.generate_content(prompt)
    answer = response.text.strip()

    return render_template("index.html", question=question, answer=answer)

if __name__ == "__main__":
    app.run(debug=True)



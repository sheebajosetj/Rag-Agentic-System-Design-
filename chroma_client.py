from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

vectordb = Chroma(
    persist_directory="db",
    embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
)


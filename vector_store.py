"""
Builds and queries a FAISS vector index over the PDF chunks using
Gemini embeddings.
"""

import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


def get_embedding_model():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY not set. Add it to your .env file."
        )
    return GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key,
    )


def build_vector_store(chunks):
    embeddings = get_embedding_model()
    store = FAISS.from_documents(chunks, embeddings)
    return store


def get_relevant_chunks(store, query, k=4):
    results = store.similarity_search(query, k=k)
    return results


def save_index(store, path="faiss_index"):
    store.save_local(path)


def load_index(path="faiss_index"):
    embeddings = get_embedding_model()
    return FAISS.load_local(
        path, embeddings, allow_dangerous_deserialization=True
    )

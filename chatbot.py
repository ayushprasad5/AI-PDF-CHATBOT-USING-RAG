"""
Core RAG logic: takes a user question, pulls the most relevant chunks
from the PDF, and asks Gemini to answer using only that context.
"""

import os
import google.generativeai as genai
from vector_store import get_relevant_chunks

PROMPT_TEMPLATE = """You are answering questions about a PDF document.
Use only the context below to answer the question. If the answer isn't
in the context, say you couldn't find that information in the document
rather than guessing.

Context:
{context}

Question: {question}

Answer:"""


def configure_gemini():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY not set. Add it to your .env file."
        )
    genai.configure(api_key=api_key)


def build_context(chunks):
    pieces = []
    for c in chunks:
        page = c.metadata.get("page", "?")
        pieces.append(f"[Page {page}]\n{c.page_content}")
    return "\n\n".join(pieces)


def answer_question(store, question, model_name="gemini-3.5-flash"):
    relevant_chunks = get_relevant_chunks(store, question, k=4)
    context = build_context(relevant_chunks)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)

    model = genai.GenerativeModel(model_name)
    response = model.generate_content(prompt)

    sources = sorted(set(c.metadata.get("page", "?") for c in relevant_chunks))
    return response.text, sources

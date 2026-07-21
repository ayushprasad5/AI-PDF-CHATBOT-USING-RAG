"""
Handles loading a PDF and splitting it into chunks small enough
to embed and search over.
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter


def load_pdf(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    return pages


def split_into_chunks(pages, chunk_size=1000, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    chunks = splitter.split_documents(pages)
    return chunks


def process_pdf(file_path):
    pages = load_pdf(file_path)
    if not pages:
        raise ValueError("No readable text found in this PDF.")
    chunks = split_into_chunks(pages)
    return chunks

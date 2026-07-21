# AI PDF Chatbot (RAG)

A chatbot that answers questions about an uploaded PDF using Retrieval-Augmented
Generation. Text is chunked, embedded, and stored in a FAISS index; relevant chunks
are retrieved for each question and passed to Gemini to generate a grounded answer.

## How it works

1. **Ingestion** (`pdf_processor.py`) — the PDF is loaded page by page and split into
   overlapping ~1000-character chunks so context isn't lost across chunk boundaries.
2. **Embedding + indexing** (`vector_store.py`) — each chunk is embedded with Gemini's
   embedding model and stored in a FAISS vector index for fast similarity search.
3. **Retrieval + generation** (`chatbot.py`) — when a question comes in, the top-k most
   similar chunks are pulled from FAISS and inserted into a prompt template, which is
   sent to Gemini so the answer is grounded in the document instead of the model's
   general knowledge.
4. **UI** (`app.py`) — a Streamlit chat interface for uploading a PDF and asking
   questions, with page numbers cited for each answer.

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key (get one from
[Google AI Studio](https://aistudio.google.com/app/apikey)):

```
GOOGLE_API_KEY=your_key_here
```

## Run

```bash
streamlit run app.py
```

Upload a PDF in the sidebar and start asking questions in the chat box.

## Notes / possible improvements

- Currently rebuilds the FAISS index per session; could persist it with
  `save_index()` / `load_index()` in `vector_store.py` to avoid re-embedding
  the same PDF on every run.
- Chunk size/overlap are fixed — could be tuned per document type (dense
  academic PDFs vs. sparse slide-style PDFs behave differently).
- No conversation memory across questions yet — each question is answered
  independently of prior turns.

# 📄 AI PDF Chatbot (RAG)

**Ask questions about any PDF and get answers grounded in the actual document — not the model's guesses.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-8E75B2?logo=googlegemini&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-blue)

A chatbot that answers questions about an uploaded PDF using **Retrieval-Augmented Generation (RAG)**. Text is chunked, embedded, and stored in a FAISS index; relevant chunks are retrieved for each question and passed to Gemini to generate a grounded, source-cited answer.

<!--
Add a screenshot or GIF here once you have one:
![App screenshot](screenshot.png)
-->

## Core Features

- Upload any PDF and chat with its contents in natural language
- Answers are grounded in the document — the model is instructed to say "not found" rather than guess
- Every answer cites the source page number(s) it was pulled from
- Clean chat interface with conversation history per session

## How It Works

1. **Ingestion** (`pdf_processor.py`) — the PDF is loaded page by page and split into overlapping ~1000-character chunks so context isn't lost across chunk boundaries.
2. **Embedding + indexing** (`vector_store.py`) — each chunk is embedded with Gemini's embedding model and stored in a FAISS vector index for fast similarity search.
3. **Retrieval + generation** (`chatbot.py`) — when a question comes in, the top-k most similar chunks are pulled from FAISS and inserted into a prompt template, which is sent to Gemini so the answer is grounded in the document instead of the model's general knowledge.
4. **UI** (`app.py`) — a Streamlit chat interface for uploading a PDF and asking questions, with page numbers cited for each answer.

```
PDF -> chunking -> embeddings -> FAISS vector index
                                      |
Question -> embedding -> similarity search -> top-k chunks
                                      |
                          Gemini generates grounded answer
```

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| UI | Streamlit |
| Orchestration | LangChain |
| Embeddings + LLM | Google Gemini API |
| Vector search | FAISS |
| PDF parsing | PyPDFLoader |

## Setup

```bash
git clone https://github.com/ayushprasad5/AI-PDF-CHATBOT-USING-RAG.git
cd AI-PDF-CHATBOT-USING-RAG
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key (get one free from [Google AI Studio](https://aistudio.google.com/app/apikey)):

```
GOOGLE_API_KEY=your_key_here
```

## Run

```bash
streamlit run app.py
```

Upload a PDF in the sidebar and start asking questions in the chat box.

## Possible Improvements

- Persist the FAISS index with `save_index()` / `load_index()` (already stubbed in `vector_store.py`) to avoid re-embedding the same PDF every session
- Tune chunk size/overlap per document type — dense academic PDFs vs. sparse slide-style PDFs behave differently
- Add conversation memory so follow-up questions can reference earlier turns
- Add basic error handling for invalid API keys, empty/scanned PDFs, and rate limits

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

# 📄 AI PDF Chatbot (RAG)

**Ask questions about any PDF and get answers grounded in the actual document — not the model's guesses.**

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?logo=langchain&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-8E75B2?logo=googlegemini&logoColor=white)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A chatbot that answers questions about an uploaded PDF using **Retrieval-Augmented Generation (RAG)**. Instead of relying on the model's general training data, the app reads the actual PDF, finds the most relevant sections for each question, and generates an answer grounded in that content — with source page numbers cited.

![App screenshot](screenshot.png)

## ✨ Features

- Upload any PDF and ask questions about its contents in plain English
- Answers are grounded in the document — the model is instructed to say "not found in this document" rather than guess or hallucinate
- Every answer cites the page number(s) it was sourced from
- Persistent chat interface with conversation history per session
- Clean, modular codebase — ingestion, embedding, retrieval, and UI are fully separated

## 🧠 How It Works

This is a standard RAG (Retrieval-Augmented Generation) pipeline:

1. **Ingestion** (`pdf_processor.py`) — the PDF is loaded page by page with `PyPDFLoader`, then split into overlapping ~1000-character chunks using LangChain's `RecursiveCharacterTextSplitter`. Overlap prevents meaning from being lost when a sentence falls across a chunk boundary.
2. **Embedding + indexing** (`vector_store.py`) — each chunk is converted into a vector embedding using Gemini's embedding model, capturing its semantic meaning. All vectors are stored in a FAISS index for fast similarity search.
3. **Retrieval** — when a question comes in, it's embedded the same way, and FAISS returns the top-k chunks whose vectors are most similar in meaning (not just matching keywords).
4. **Generation** (`chatbot.py`) — the retrieved chunks are inserted into a prompt template along with the question and sent to Gemini, which generates an answer using only that context.
5. **UI** (`app.py`) — a Streamlit chat interface handles PDF upload, indexing status, and the conversational Q&A loop.

```
PDF → chunking → embeddings → FAISS vector index
                                      │
Question → embedding → similarity search → top-k relevant chunks
                                      │
                          Gemini generates a grounded, cited answer
```

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Language | Python | Core implementation |
| UI | Streamlit | Chat interface, file upload |
| Orchestration | LangChain | PDF loading, chunking, embedding wrappers |
| Embeddings + LLM | Google Gemini API | Semantic embeddings + answer generation |
| Vector search | FAISS | Fast similarity search over embeddings |
| PDF parsing | PyPDFLoader | Text extraction from PDF pages |

## 🚀 Setup

```bash
git clone https://github.com/ayushprasad5/AI-PDF-CHATBOT-USING-RAG.git
cd AI-PDF-CHATBOT-USING-RAG
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your Gemini API key (free from [Google AI Studio](https://aistudio.google.com/app/apikey)):

```
GOOGLE_API_KEY=your_key_here
```

## ▶️ Run

```bash
streamlit run app.py
```

Upload a PDF in the sidebar, wait for indexing to finish, and start asking questions in the chat box.

## 📁 Project Structure

```
├── app.py              # Streamlit UI and chat loop
├── pdf_processor.py     # PDF loading and chunking
├── vector_store.py       # Embeddings and FAISS index
├── chatbot.py             # Retrieval + prompt construction + generation
├── requirements.txt
├── .env.example
└── LICENSE
```

## 🔭 Possible Improvements

- Persist the FAISS index to disk (`save_index()` / `load_index()` are already stubbed in `vector_store.py`) instead of re-embedding the same PDF every session
- Tune chunk size/overlap per document type — dense academic PDFs vs. sparse slide decks behave differently
- Add conversation memory so follow-up questions can reference earlier turns
- Add explicit error handling for invalid API keys, empty/scanned PDFs, and API rate limits

## 📄 License

Licensed under the MIT License — see [LICENSE](LICENSE) for details.

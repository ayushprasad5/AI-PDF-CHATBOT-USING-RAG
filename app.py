import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from pdf_processor import process_pdf
from vector_store import build_vector_store, save_index, load_index
from chatbot import configure_gemini, answer_question

load_dotenv()

st.set_page_config(page_title="PDF Chatbot", page_icon="📄", layout="wide")

if "store" not in st.session_state:
    st.session_state.store = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "file_name" not in st.session_state:
    st.session_state.file_name = None

st.title("📄 PDF Chatbot")
st.caption("Upload a PDF and ask questions about its contents.")

with st.sidebar:
    st.header("Upload")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file is not None and uploaded_file.name != st.session_state.file_name:
        with st.spinner("Reading and indexing the document..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                tmp.write(uploaded_file.read())
                tmp_path = tmp.name

            try:
                configure_gemini()

                index_path = f"faiss_index_{uploaded_file.name}"
                if os.path.exists(index_path):
                    st.session_state.store = load_index(index_path)
                else:
                    chunks = process_pdf(tmp_path)
                    st.session_state.store = build_vector_store(chunks)
                    save_index(st.session_state.store, index_path)

                st.session_state.file_name = uploaded_file.name
                st.session_state.chat_history = []
                st.success(f"Indexed {uploaded_file.name}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
            finally:
                os.remove(tmp_path)

    if st.session_state.file_name:
        st.info(f"Active document: {st.session_state.file_name}")
        if st.button("Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

if st.session_state.store is None:
    st.write("Upload a PDF from the sidebar to get started.")
else:
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    question = st.chat_input("Ask something about the document...")
    if question:
        st.session_state.chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, sources = answer_question(st.session_state.store, question)
                    source_note = f"\n\n*Sources: page(s) {', '.join(str(s) for s in sources)}*"
                    full_answer = answer + source_note
                    st.write(full_answer)
                    st.session_state.chat_history.append(
                        {"role": "assistant", "content": full_answer}
                    )
                except Exception as e:
                    st.error(f"Error generating a response: {e}")

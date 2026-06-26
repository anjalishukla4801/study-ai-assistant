import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="ChatBot", page_icon=None, layout="wide")

import styles
import sys
import os

# Ensure we can import styles if it's in the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import styles
current_theme = styles.display_theme_toggle()
styles.apply_custom_styles(current_theme)

# --- 1. SETUP RAG AND GROQ ---
try:
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    
    # Import RAG components
    from rag.embeddings import RAGEmbeddings
    from rag.vector_store import RAGVectorStore
    from rag.retriever import RAGRetriever
    from rag.llm import GroqLLM
    
    embeddings_model = RAGEmbeddings()
    vector_store = RAGVectorStore(persist_directory="vector_db")
    retriever = RAGRetriever(embeddings=embeddings_model, vector_store=vector_store)
    llm = GroqLLM(api_key=api_key)
except Exception as e:
    st.error(f"🚨 Setup Error: {e}")
    st.stop()

if "pdf_hash" not in st.session_state:
    st.warning("🚨 No notes found! Please upload a PDF on the Home page first.")
    st.stop()

st.title("Chat with Your Notes")
st.markdown("Ask questions and get instant answers based on your uploaded document.")

# --- 2. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    avatar = None
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 3. HANDLE USER INPUT ---
if prompt := st.chat_input("Ask a question about your notes..."):
    with st.chat_message("user", avatar=None):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar=None):
        with st.spinner("Thinking..."):
            try:
                # 1. Retrieve top 5 relevant chunks from ChromaDB
                pdf_hash = st.session_state.pdf_hash
                retrieved_chunks = retriever.retrieve(pdf_hash, prompt, top_k=5)
                
                # 2. Extract last 4 messages for conversational history
                chat_history = []
                # Exclude the message we just appended (the current prompt)
                history_msgs = st.session_state.messages[:-1]
                for msg in history_msgs[-4:]:
                    chat_history.append({"role": msg["role"], "content": msg["content"]})
                
                # 3. Call RAG LLM
                response = llm.generate_answer(
                    query=prompt,
                    retrieved_chunks=retrieved_chunks,
                    chat_history=chat_history
                )
                
                st.markdown(response)
                
                # Save response
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {e}")
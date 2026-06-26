import streamlit as st
import PyPDF2
import hashlib

# Import RAG components
from rag.pdf_loader import PDFLoader
from rag.chunker import RAGChunker
from rag.embeddings import RAGEmbeddings
from rag.vector_store import RAGVectorStore

st.set_page_config(page_title="Study AI", page_icon=None, layout="wide")

import styles
current_theme = styles.display_theme_toggle()
styles.apply_custom_styles(current_theme)

# --- HERO SECTION ---
col1, col2 = st.columns([3, 1])

with col1:
    st.title("Study AI Assistant")
    st.markdown("""
        <div style="padding-bottom: 2rem;">
            <h3 style="font-weight: 400; color: #64748b;">Unlock your potential with smart study tools.</h3>
            <p style="font-size: 1.1rem;">
                Upload your study materials and instantly access an AI-powered Chatbot, 
                Flashcards generator, and Quiz Master to master your subjects.
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- 1. FILE UPLOADER SECTION ---
st.divider()
st.subheader("1. Upload Your Notes")

# Centering the uploader slightly or making it prominent
with st.container():
    uploaded_file = st.file_uploader("Upload your PDF document to get started", type=["pdf"], label_visibility="collapsed")

if uploaded_file is not None:
    # --- 2. EXTRACT TEXT & RAG INDEXING ---
    with st.spinner("Processing document..."):
        try:
            # A. Compute file hash
            file_bytes = uploaded_file.getvalue()
            pdf_hash = hashlib.sha256(file_bytes).hexdigest()
            st.session_state.pdf_hash = pdf_hash
            
            # B. Extract full raw text for legacy Flashcards/Quizzes (so they are unaffected)
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
            st.session_state.pdf_text = text
            
            # C. Check ChromaDB collection and index if new
            vector_store = RAGVectorStore(persist_directory="vector_db")
            
            if vector_store.collection_exists_and_populated(pdf_hash):
                st.success(f"Document processed. (Loaded existing embeddings for {uploaded_file.name})")
            else:
                # Load page-by-page
                pages = PDFLoader.load(uploaded_file)
                
                # Chunk
                chunker = RAGChunker(chunk_size=700, chunk_overlap=150)
                chunks = chunker.chunk_documents(pages)
                
                if not chunks:
                    raise ValueError("Document yielded 0 chunks. Cannot embed empty content.")
                
                # Embed
                embeddings_model = RAGEmbeddings()
                chunk_texts = [item["text"] for item in chunks]
                embeddings = embeddings_model.embed_documents(chunk_texts)
                
                # Add to Vector DB
                vector_store.add_chunks(pdf_hash, chunks, embeddings)
                st.success(f"Document processed. {len(pdf_reader.pages)} pages loaded, split into {len(chunks)} chunks, and saved to database.")
            
            # Action Cards
            st.divider()
            st.subheader("2. Choose Your Tool")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.page_link("pages/chatbot.py", label="Study Chatbot", use_container_width=True)
                st.caption("Ask questions about your notes.")
            with c2:
                st.page_link("pages/Flashcards.py", label="Generate Flashcards", use_container_width=True)
                st.caption("Create cards for memorization.")
            with c3:
                st.page_link("pages/Quiz_master.py", label="Quiz Master", use_container_width=True)
                st.caption("Test your knowledge.")
            
        except Exception as e:
            st.error(f"Error processing PDF: {e}")

# --- 4. SIDEBAR INFO ---
with st.sidebar:
    st.title("Study AI")
    st.divider()
    st.markdown("**Model:** Llama-3 (Groq)")
    
    st.markdown("### Status")
    if "pdf_text" in st.session_state:
        st.info("Document Loaded")
    else:
        st.write("No document uploaded")
        
    st.divider()
    st.caption("Study AI Assistant")

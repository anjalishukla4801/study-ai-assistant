import streamlit as st
from groq import Groq
import json
import pandas as pd
import os

st.set_page_config(page_title="Flashcards", page_icon=None, layout="wide")

import styles
import sys
import os

# Ensure we can import styles if it's in the parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import styles
current_theme = styles.display_theme_toggle()
styles.apply_custom_styles(current_theme)

# --- 1. SETUP GROQ AND RAG ---
try:
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
    
    from rag.embeddings import RAGEmbeddings
    from rag.vector_store import RAGVectorStore
    from rag.retriever import RAGRetriever
    
    embeddings_model = RAGEmbeddings()
    vector_store = RAGVectorStore(persist_directory="vector_db")
    retriever = RAGRetriever(embeddings=embeddings_model, vector_store=vector_store)
except Exception as e:
    st.error(f"🚨 Setup Error: {e}")
    st.stop()

if "pdf_hash" not in st.session_state:
    st.warning("🚨 Upload notes first!")
    st.stop()

st.title("Smart Flashcards")
st.markdown("Generate flashcards from your notes to help you memorize key concepts.")

# --- 2. GENERATE BUTTON ---
if st.button("Generate Flashcards"):
    with st.spinner("Analyzing text..."):
        try:
            # Use RAG to sample 8 diverse chunks across the entire document
            diverse_chunks = retriever.get_diverse_chunks(st.session_state.pdf_hash, num_chunks=8)
            safe_text = "\n\n".join([c["text"] for c in diverse_chunks])
            
            prompt = f"""
            Extract 10 key terms and definitions from this text:
            {safe_text}
            
            Return a JSON Array ONLY. Format:
            [
                {{"term": "Concept", "def": "Definition"}}
            ]
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            
            # Clean and Parse JSON
            raw_json = completion.choices[0].message.content
            clean_json = raw_json.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            # Save to session state to persist
            st.session_state.flashcards = data
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- 3. DISPLAY FLASHCARDS ---
if "flashcards" in st.session_state:
    st.divider()
    st.subheader("Your Flashcards")
    
    # Grid Layout
    cols = st.columns(2)
    
    for i, card in enumerate(st.session_state.flashcards):
        # coloring alternating cards slightly differently or just using the card style
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div class="custom-card">
                    <h4 style="margin:0; font-weight: 600;">{card['term']}</h4>
                    <p style="margin-top: 0.5rem; color: #64748b;">{card['def']}</p>
                </div>
                """, unsafe_allow_html=True)

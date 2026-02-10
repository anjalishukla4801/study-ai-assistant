import streamlit as st
from groq import Groq
import json
import pandas as pd
import os

st.set_page_config(page_title="Flashcards", page_icon="⚡")

# --- 1. SETUP GROQ ---
try:
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except:
    st.error("🚨 Groq API Key Missing")
    st.stop()

if "pdf_text" not in st.session_state:
    st.warning("🚨 Upload notes first!")
    st.stop()

st.title("⚡ Smart Flashcards")

# --- 2. GENERATE BUTTON ---
if st.button("🚀 Generate Flashcards"):
    with st.spinner("Analyzing text..."):
        try:
            # SAFETY LIMIT
            safe_text = st.session_state.pdf_text[:15000]
            
            prompt = f"""
            Extract 5 key terms and definitions from this text:
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
            
            # Display as a nice Table
            st.write("### 📝 Key Terms")
            df = pd.DataFrame(data)
            st.table(df)
            
        except Exception as e:
            st.error(f"Error: {e}")
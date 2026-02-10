import streamlit as st
import PyPDF2

st.set_page_config(page_title="Study AI", page_icon="🎓", layout="wide")

st.title("🎓 AI Study Assistant")
st.subheader("Upload your notes and let AI do the rest.")

# --- 1. FILE UPLOADER ---
uploaded_file = st.file_uploader("Upload a PDF Document", type=["pdf"])

if uploaded_file is not None:
    # --- 2. EXTRACT TEXT ---
    with st.spinner("Processing PDF..."):
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            
            # Save to Session State (so other pages can use it)
            st.session_state.pdf_text = text
            
            # --- 3. SUCCESS MESSAGE ---
            st.success(f"✅ PDF Processed! Loaded {len(pdf_reader.pages)} pages.")
            st.info("👈 Now go to the sidebar and choose 'Chatbot', 'Flashcards', or 'Quiz'.")
            
        except Exception as e:
            st.error(f"Error reading PDF: {e}")

# --- 4. SIDEBAR INFO ---
with st.sidebar:
    st.info("🚀 **Model:** Llama-3 (via Groq)")
    if "pdf_text" in st.session_state:
        st.success("📂 PDF Loaded")
    else:
        st.warning("📂 No PDF Loaded")
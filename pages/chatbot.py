import streamlit as st
from groq import Groq
import os

st.set_page_config(page_title="ChatBot", page_icon="🤖")

# --- 1. SETUP GROQ ---
try:
    api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
    client = Groq(api_key=api_key)
except Exception as e:
    st.error("🚨 Groq API Key is missing! Check your secrets.")
    st.stop()

if "pdf_text" not in st.session_state:
    st.warning("🚨 No notes found! Please upload a PDF on the Home page first.")
    st.stop()

st.title("🤖 Chat with Llama-3")

# --- 2. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# --- 3. HANDLE USER INPUT ---
if prompt := st.chat_input("Ask a question about your notes..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # SAFETY: Limit context to avoid crashing Groq (approx 15k chars)
                context_text = st.session_state.pdf_text[:15000]
                
                # Create the conversation for the API
                chat_history = [
                    {"role": "system", "content": f"You are a helpful study assistant. Answer based on this text:\n\n{context_text}"}
                ]
                # Add previous chat history (last 4 messages to save space)
                chat_history.extend(st.session_state.messages[-4:])
                
                # Call Groq
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=chat_history,
                    temperature=0.5,
                    max_tokens=500
                )
                
                response = completion.choices[0].message.content
                st.markdown(response)
                
                # Save response
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"Error: {e}")
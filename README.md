# 🎓 Study AI Assistant

**Transform your boring PDF notes into an interactive study engine.**

Study AI Assistant is a Streamlit-based web application that uses **Llama-3 (via Groq)** to turn static PDF documents into active learning tools. Upload your course notes, and instantly get a chatbot, quizzes, and flashcards generated from your content.

🔗 **Live Demo:** [Click here to view the App](https://study-ai-assistant.streamlit.app/) *(Replace with your actual link)*

---

## 🚀 Features

### 1. 🤖 AI Chatbot (RAG)
* Ask questions directly to your PDF.
* The AI reads your document and answers based **only** on the context provided.
* No hallucinations—strict adherence to your source material.

### 2. ❓ Quiz Master
* Generate **Multiple Choice** or **True/False** questions instantly.
* Customizable difficulty (Easy, Medium, Hard).
* Get immediate feedback and explanations for every answer.

### 3. ⚡ Smart Flashcards
* Automatically extracts key terms and definitions from your notes.
* Perfect for last-minute revision and memorization.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Python)
* **LLM Engine:** [Llama-3.3-70b-versatile](https://groq.com/) (via Groq API)
* **PDF Processing:** PyPDF2
* **Deployment:** Streamlit Community Cloud

---

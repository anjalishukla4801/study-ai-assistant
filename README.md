# Study AI Assistant

A professional, high-performance study companion powered by AI. Transform your study materials into interactive learning modules instantly.

[Live Demo](https://study-ai-assistant.streamlit.app/)

---

## Overview

Study AI Assistant automates the most time-consuming parts of learning. By leveraging a state-of-the-art **Retrieval-Augmented Generation (RAG)** pipeline, it converts standard PDF notes into a suite of powerful study tools including interactive chatbots, randomized flashcards, and customized knowledge tests. The application chunks, embeds, and stores documents locally to retrieve highly relevant context, enabling accurate answers with automatic source citation.

## Core Features

### 1. RAG-Powered Chatbot
Engage in a context-aware dialogue with your study materials. The chatbot retrieves the most relevant chunks from your document to answer complex questions, summarize sections, and clarify difficult concepts—complete with **verified source citations** (filename and page numbers).

### 2. Smart Flashcards
Instantly generate high-quality flashcards. The AI uses semantic sampling across different sections of your notes (beginning, middle, and end) to identify key terms and definitions, creating a well-structured review system to accelerate memorization.

### 3. Quiz Master
Generate dynamically structured practice exams. Customize your knowledge assessment with multiple difficulty levels and support for both Multiple Choice and True/False formats, drawing questions semantically distributed across the entire document.

### 4. Professional Design
A minimalist, high-performance interface designed for focus. Features include:
- Clean, icon-free professional aesthetic.
- Seamless Dark and Light theme optimization.
- Responsive, mobile-friendly layouts.

---

## Technical Architecture

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Large Language Model**: [Llama-3 (llama-3.3-70b-versatile) via Groq API](https://groq.com/)
- **Vector Database**: [ChromaDB](https://www.trychroma.com/) for local embedding storage and metadata querying
- **Embeddings**: `all-MiniLM-L6-v2` via [SentenceTransformers](https://sbert.net/)
- **Text Splitting**: [LangChain Text Splitters](https://github.com/langchain-ai/langchain) for recursive character chunking
- **PDF Processing**: [PyPDF2](https://pypdf2.readthedocs.io/)
- **Data Handling**: [Pandas](https://pandas.pydata.org/)

---

## Installation and Local Setup

### Prerequisites
- Python 3.8 or higher
- A Groq Cloud API Key

### 1. Clone the Repository
```bash
git clone https://github.com/anjalishukla4801/study-ai-assistant.git
cd study-ai-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Secrets
Create a `.streamlit/secrets.toml` file in the project root:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

### 4. Launch the Application
```bash
python -m streamlit run Home.py
```

---

## Usage Guide

1. **Upload**: Drop your PDF notes on the Home page.
2. **Process**: Wait for the successful document extraction notification.
3. **Master**: Navigate to the Tool selection area and choose your preferred study method.

---

> [!TIP]
> **Pro Tip**: Use the Quiz Master on "Hard" difficulty for deeper conceptual reinforcement after reviewing with Flashcards.

---

*Made with dedication to efficient learning.*

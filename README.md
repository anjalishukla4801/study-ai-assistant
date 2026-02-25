# Study AI Assistant

A professional, high-performance study companion powered by AI. Transform your study materials into interactive learning modules instantly.

[Live Demo](https://study-ai-assistant.streamlit.app/)

---

## Overview

Study AI Assistant automates the most time-consuming parts of learning. By leveraging advanced Large Language Models (LLMs), it converts standard PDF notes into a suite of powerful study tools including interactive chatbots, randomized flashcards, and customized knowledge tests.

## Core Features

### 1. Intelligent Chatbot
Engage in a context-aware dialogue with your study materials. The chatbot uses the full context of your uploaded document to answer complex questions, summarize sections, and clarify difficult concepts.

### 2. Smart Flashcards
Instantly generate high-quality flashcards. The AI identifies key terms and definitions within your notes, creating a structured review system to accelerate memorization.

### 3. Quiz Master
Generate dynamically structured practice exams. Customize your knowledge assessment with multiple difficulty levels and support for both Multiple Choice and True/False formats, complete with instant scoring and explanations.

### 4. Professional Design
A minimalist, high-performance interface designed for focus. Features include:
- Clean, icon-free professional aesthetic.
- Seamless Dark and Light theme optimization.
- Responsive, mobile-friendly layouts.

---

## Technical Architecture

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Large Language Model**: [Llama-3 via Groq API](https://groq.com/)
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

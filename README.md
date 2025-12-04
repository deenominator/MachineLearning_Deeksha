# GDGC Info Chatbot

A RAG (Retrieval-Augmented Generation) chatbot designed for the Google Developer Groups on Campus (GDGC). This bot helps members finding information about events, teams, and membership details, and allows users to submit support tickets.

## Features
- **RAG Implementation**: Retrieves relevant context from club data using FAISS and SentenceTransformers.
- **LLM Integration**: Generates human-like responses using OpenRouter (Gemma-2-9b-it).
- **Ticket System**: Automatically logs user issues into a CSV file.
- **Interactive UI**: Built with Streamlit for a chat-like experience.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

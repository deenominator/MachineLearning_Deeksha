import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def call_llm(context_chunks, user_query):
    """
    Sends the RAG context + user query to OpenRouter LLM.
    """

    context = "\n\n".join(context_chunks)

    prompt = f"""
 You are GDGC InfoBot. Use ONLY the information in the context below.
 If the answer is not found in the context, say:
 "I'm sorry, I don't have information about that."

CONTEXT:
{context}

USER QUESTION:
{user_query}

ANSWER:
"""

    payload = {
        "model": "google/gemma-2-9b-it",
        "messages": [
            {"role": "system", "content": "Answer using ONLY the provided context."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }

    response = requests.post(OPENROUTER_URL, json=payload, headers=HEADERS)

    if response.status_code != 200:
        return f"Error: {response.text}"

    return response.json()["choices"][0]["message"]["content"]

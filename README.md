# GDGC Info Chatbot
## Live link: https://machinelearningdeeksha-gdgc.streamlit.app/
**GDGC Info Chatbot** is an AI-powered assistant designed for **Google Developer Groups on Campus (VIT Bhopal)**. It helps students navigate club activities, offering specific workflows for members and non-members, and provides a direct line of support through a ticketing system.

## Key Features

### 1. Smart User Segmentation
Upon launching, the bot asks if you are a current GDGC member:
* **For Non-Members:** The bot provides a warm **Introductory Message**, explaining what GDGC is, our vision, and how to get involved.
* **For Members:** Users get a personalized experience. They can optionally enter their **Name** and **Team** (e.g., Web Dev, ML, Design) to receive a custom greeting.

### 2. AI-Powered Queries (RAG)
Powered by **RAG (Retrieval-Augmented Generation)**, the bot answers questions using actual club data. It provides accurate information on:
* Upcoming events and workshops.
* **Club Leadership:** You can ask for the **Lead and Co-Lead** details to get in contact with them directly.
* Membership benefits and team structures.

### 3. Support Ticket System
If the AI cannot resolve a specific query or if you face an issue, the bot allows you to **raise a support ticket**.
* Tickets are logged with a timestamp and ID.
* Admins can review `tickets.csv` to resolve pending issues.

## Tech Stack
* **Frontend:** Streamlit
* **LLM Integration:** OpenRouter API (Gemma-2-9b-it)
* **Vector Search:** FAISS (Facebook AI Similarity Search)
* **Embeddings:** SentenceTransformers (`all-MiniLM-L6-v2`)

## Future Enhancements
We are constantly working to improve the bot. Planned features include:
* ** Enhanced UI:** A more polished, modern chat interface.
* ** Emotion Detection:** Analyzing user sentiment to provide more empathetic responses.
* ** Event Integration:** Real-time calendar syncing for upcoming events.

##  Installation & Setup

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-link>
    cd <your-repo-name>
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your OpenRouter API key:
    ```
    OPENROUTER_API_KEY=your_api_key_here
    ```

4.  **Build the Knowledge Base**
    Process the club data and create the FAISS index:
    ```bash
    python build_index.py
    ```

5.  **Run the App**
    ```bash
    streamlit run app.py
    ```
    <img width="1365" height="602" alt="image" src="https://github.com/user-attachments/assets/39186f07-19e9-4176-ae87-4d23b714e8d8" />
    
    <img width="1356" height="585" alt="image" src="https://github.com/user-attachments/assets/c5181130-a91e-4fe2-91f5-27cdccd40e75" />

    <img width="988" height="521" alt="image" src="https://github.com/user-attachments/assets/6aaf1ca1-303b-431c-8bc6-589feee1d71c" />

    <img width="1365" height="558" alt="image" src="https://github.com/user-attachments/assets/2f52c0be-fc55-4116-989c-dd85cb214108" />

    <img width="954" height="381" alt="image" src="https://github.com/user-attachments/assets/3aa6f31d-d317-4c55-baf8-efb7db45b45b" />


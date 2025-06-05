# GPTLocal
# 🧠 Mental Health RAG Chatbot (Offline GPT with Mistral + Chroma)

A fully offline, private, and intelligent chatbot powered by:
- 🧠 [Mistral-7B](https://ollama.com/library/mistral) — a lightweight open-source LLM
- 📚 ChromaDB — a blazing-fast local vector database
- 🧩 SentenceTransformers — for generating embeddings
- 💬 Gradio — beautiful chat interface

> 🛠 Built for mental health queries using domain-specific data from Reddit and beyond.

---

## 🚀 Features

- ✅ Works 100% locally — no OpenAI API needed
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Uses your own data (Reddit, PDFs, etc.)
- 💬 ChatGPT-style interface with Gradio
- 🧱 Modular code for easy customization

---


---

## 📦 Tech Stack

| Tool              | Purpose                                      |
|-------------------|----------------------------------------------|
| **Mistral (via Ollama)** | Local LLM for answering queries     |
| **ChromaDB**      | Vector store for semantic search              |
| **SentenceTransformers** | Converts text into vector embeddings |
| **Gradio**        | Chat frontend                                |
| **PRAW** *(optional)* | Scrape mental health Reddit data       |

---

2. Install Dependencies

pip install -r requirements.txt

3. Install & Start Ollama

curl -fsSL https://ollama.com/install.sh | sh
ollama run mistral

4. Run ChromaDB Server

chroma run --path chroma_db/

🧠 Index Your Data

Run the indexing script to embed your documents:

python rag_preprocess_and_index.py

    Customize this script to embed Reddit, PDFs, or any text files.

💬 Start the Chatbot

python app.py

    This will launch the Gradio chat UI in your browser.

📁 Project Structure

├── app.py                  # Gradio frontend & chatbot logic
├── rag_query_local_mistral.py # Main RAG logic (retrieval + Mistral)
├── rag_preprocess_and_index.py # Embed and store docs in ChromaDB
├── chroma_db/              # Local vector database files
├── data/                   # Your source content (JSON, etc.)
├── requirements.txt
└── README.md

🎯 Future Ideas

    Add memory to continue multi-turn conversations

    Plug in tools (calculator, search) with LangChain

    Create domain-specific AI assistants

📜 License

MIT — free to use, modify, and share.
🧠 Inspired by

    Ollama

    Chroma

    Gradio

    The open-source AI community 🙌

🙋 Need Help?

Open an issue or ping me on dev.ios.amit@gmail.com.

    




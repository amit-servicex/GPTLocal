import gradio as gr
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import requests

# Setup Chroma connection
client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_collection("mental_health_rag")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Main RAG chat function
def rag_chat(user_message, chat_history):
    if not user_message:
        return "", chat_history

    # Step 1: Embed query
    query_embedding = model.encode(user_message).tolist()

    # Step 2: Retrieve from Chroma
    results = collection.query(query_embeddings=[query_embedding], n_results=3)
    docs = results["documents"][0]
    context = "\n---\n".join(docs)

    # Step 3: Format prompt
    prompt = f"""You are a mental health support assistant.
Answer kindly and supportively using the context below.

Context:
{context}

User: {user_message}
Assistant:"""

    # Step 4: Query Ollama (Mistral)
    try:
        res = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        reply = res.json().get("response", "").strip()
    except Exception as e:
        reply = f"❌ Error querying LLM: {e}"

    # Step 5: Update chat history
    chat_history.append((user_message, reply))
    return "", chat_history

# Launch Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Mental Health Copilot Chat")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type how you're feeling today...")
    clear = gr.Button("Clear chat")
    state = gr.State([])

    msg.submit(rag_chat, [msg, state], [msg, chatbot])
    clear.click(lambda: ([], ""), None, [state, msg, chatbot])

demo.launch()

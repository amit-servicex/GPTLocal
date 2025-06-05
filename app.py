import gradio as gr
import requests
from chromadb import HttpClient

# Connect to Chroma server
chroma_client = HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection("mental_health_rag")

# Retrieve relevant documents
def get_context(query):
    results = collection.query(query_texts=[query], n_results=5)
    return "\n".join(results["documents"][0]) if results["documents"] else ""

# Ask Mistral via Ollama
def ask_mistral(context, history, query):
    past = "\n".join([f"User: {q}\nAI: {a}" for q, a in history])
    prompt = f"""You are a helpful mental health assistant.

Context:
{context}

Conversation so far:
{past}

User: {query}
AI:"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": "mistral",
        "prompt": prompt,
        "stream": False
    })

    print("\n====== Final Prompt to Mistral ======\n")
    print(prompt)
    print("\n=====================================\n")

    return response.json()["response"].strip()

# Gradio Chat Handler
def chat_fn(message, history):
    context = get_context(message)
    answer = ask_mistral(context, history, message)
    history.append((message, answer))
    return "", history

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## 🧠 Local Mental Health Chat (Mistral + RAG)")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type a question and hit Enter...")
    state = gr.State([])

    msg.submit(chat_fn, inputs=[msg, state], outputs=[msg, chatbot])

demo.launch()

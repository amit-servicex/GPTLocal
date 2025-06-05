from chromadb import HttpClient
from sentence_transformers import SentenceTransformer
import requests

COLLECTION_NAME = "mental_health_rag"

# ✅ Connect to Chroma server
client = HttpClient(host="localhost", port=8000)
collection = client.get_collection(COLLECTION_NAME)

# ✅ Embed user query
model = SentenceTransformer("all-MiniLM-L6-v2")
query = input("💬 Ask your Copilot: ").strip()
query_embedding = model.encode(query).tolist()

# ✅ Retrieve
results = collection.query(query_embeddings=[query_embedding], n_results=3)
retrieved_docs = results["documents"][0]
context = "\n---\n".join(retrieved_docs)

# ✅ Send to Mistral (via Ollama)
prompt = f"""You are a kind and empathetic mental health assistant.
Use the following related conversations to guide your response:

{context}

User: {query}
Assistant:"""

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "mistral", "prompt": prompt, "stream": False}
)

print("\n💡 Response:\n", response.json()["response"].strip())

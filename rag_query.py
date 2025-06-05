import chromadb
from sentence_transformers import SentenceTransformer
import openai

# Setup
model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.Client()
collection = chroma_client.get_collection("mental_health_rag")

# OpenAI config (or use local LLM)
openai.api_key = "YOUR_OPENAI_KEY"

query = input("🧠 Ask something: ")

# Step 1: Embed query
query_embedding = model.encode(query).tolist()

# Step 2: Retrieve from Chroma
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

retrieved_docs = results["documents"][0]

# Step 3: Use OpenAI to answer
context = "\n---\n".join(retrieved_docs)
prompt = f"""You are a kind and empathetic mental health assistant.
Use the following conversations to help answer the user's concern:

{context}

User: {query}
Assistant:"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.6
)

print("\n💬 Copilot Response:")
print(response["choices"][0]["message"]["content"])

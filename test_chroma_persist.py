import chromadb
from chromadb.config import Settings

# ✅ Connect to ChromaDB with disk persistence
client = chromadb.Client(Settings(persist_directory="chroma_db"))

# ✅ Use get_or_create_collection (DO NOT DELETE!)
collection = client.get_or_create_collection("test_collection")

# ✅ Only add if not already added (avoid duplicate error)
try:
    collection.add(
        documents=["This is a test document about mental health."],
        ids=["doc1"],
        metadatas=[{"source": "test"}]
    )
    print("✅ Document added and should persist.")
except Exception as e:
    print("⚠️ Probably already added:", e)

# ✅ Show all collections
print("\n📦 Collections:")
for col in client.list_collections():
    print("-", col.name)

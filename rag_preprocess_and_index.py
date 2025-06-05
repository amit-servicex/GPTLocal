import pandas as pd
from sentence_transformers import SentenceTransformer
from chromadb import HttpClient

CSV_FILE = "chromadb_ready_data.csv"
COLLECTION_NAME = "mental_health_rag"
BATCH_SIZE = 64

# ✅ Connect to Chroma server (running in another terminal)
chroma_client = HttpClient(host="localhost", port=8000)
collection = chroma_client.get_or_create_collection(COLLECTION_NAME)

# ✅ Load cleaned CSV
df = pd.read_csv(CSV_FILE).dropna(subset=["text"])
print(f"📄 Loaded {len(df)} rows")

# ✅ Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# ✅ Prepare data
texts = df["text"].tolist()
ids = df["id"].tolist()
sources = df["source"].tolist()

# ✅ Batch index
for i in range(0, len(texts), BATCH_SIZE):
    batch_texts = texts[i:i + BATCH_SIZE]
    batch_ids = ids[i:i + BATCH_SIZE]
    batch_sources = sources[i:i + BATCH_SIZE]

    embeddings = model.encode(batch_texts)

    collection.add(
        documents=batch_texts,
        embeddings=[e.tolist() for e in embeddings],
        ids=batch_ids,
        metadatas=[{"source": src} for src in batch_sources]
    )

print(f"\n✅ Done. Indexed and persisted to ChromaDB server.")

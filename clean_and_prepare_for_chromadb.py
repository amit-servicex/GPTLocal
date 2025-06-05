import os
import pandas as pd

# Input CSVs and their source labels
csv_inputs = [
    ("amod_mental_health_counseling_conversations.csv", "amod"),
    ("reddit_mental_health_posts.csv", "reddit"),
    ("mental_health_chatbot_dataset.csv", "chatbot"),
]

# Output file
output_file = "chromadb_ready_data.csv"
rows = []

def extract_clean_text(row, source):
    try:
        if source == "amod":
            return row.get("dialogue", "").strip()

        elif source == "reddit":
            title = str(row.get("title", "")).strip()
            body = str(row.get("selftext", "")).strip()
            comments = str(row.get("top_comments", row.get("comments", ""))).strip()
            return f"{title}\n{body}\n{comments}".strip()

        elif source == "chatbot":
            query = str(row.get("query", "")).strip()
            response = str(row.get("response", "")).strip()
            return f"User: {query}\nBot: {response}".strip()
    except Exception as e:
        return None

# Process each dataset
doc_id = 0
for path, source in csv_inputs:
    if not os.path.exists(path):
        print(f"⚠️ File not found: {path}")
        continue

    print(f"📦 Processing {path}")
    df = pd.read_csv(path).fillna("")

    for _, row in df.iterrows():
        text = extract_clean_text(row, source)
        if text and len(text) > 30:
            rows.append({
                "id": f"{source}_{doc_id}",
                "text": text,
                "source": source
            })
            doc_id += 1

# Save cleaned output
df_out = pd.DataFrame(rows)
df_out.to_csv(output_file, index=False, encoding="utf-8")

print(f"\n✅ Cleaned and saved {len(df_out)} rows to {output_file}")

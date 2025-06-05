import os
import json
import pandas as pd
from datasets import load_dataset

# Configurable dataset list
DATASETS_TO_DOWNLOAD = [
    {
        "name": "Amod/mental_health_counseling_conversations",
        "split": "train",
        "csv_file": "amod_mental_health_counseling_conversations.csv"
    },
    {
        "name": "solomonk/reddit_mental_health_posts",
        "split": "train",
        "csv_file": "reddit_mental_health_posts.csv"
    },
    {
        "name": "heliosbrahma/mental_health_chatbot_dataset",
        "split": "train",
        "csv_file": "mental_health_chatbot_dataset.csv"
    }
]

# Metadata file to track row counts and last update
METADATA_FILE = "dataset_metadata.json"

# Load previous metadata if exists
if os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "r") as f:
        dataset_metadata = json.load(f)
else:
    dataset_metadata = {}

# Start downloading/updating
for ds in DATASETS_TO_DOWNLOAD:
    name = ds["name"]
    split = ds["split"]
    csv_file = ds["csv_file"]

    print(f"\n📥 Checking dataset: {name}")

    # Load full dataset
    try:
        dataset = load_dataset(name, split=split)
        df = pd.DataFrame(dataset)
        remote_row_count = len(df)
    except Exception as e:
        print(f"❌ Failed to load {name}: {e}")
        continue

    # Compare with local metadata
    prev_meta = dataset_metadata.get(name)
    local_exists = os.path.exists(csv_file)

    if prev_meta and local_exists:
        previous_row_count = prev_meta.get("rows", 0)
        if remote_row_count == previous_row_count:
            print(f"✅ No new data. Skipping download (rows: {remote_row_count})")
            continue
        else:
            print(f"🔄 Data updated! Old rows: {previous_row_count}, New rows: {remote_row_count}")
    else:
        print(f"🆕 New dataset or missing local file.")

    # Save new/updated CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")
    print(f"💾 Saved to {csv_file}")

    # Update metadata
    dataset_metadata[name] = {
        "rows": remote_row_count,
        "last_fetched": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Write updated metadata
with open(METADATA_FILE, "w") as f:
    json.dump(dataset_metadata, f, indent=2)

print("\n✅ All datasets processed and metadata updated.")

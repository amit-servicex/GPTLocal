import requests
import json
import time
import csv

# API config
DATASET = "solomonk/reddit_mental_health_posts"
BASE_URL = "https://datasets-server.huggingface.co/rows"
CONFIG = "default"
SPLIT = "train"
CHUNK_SIZE = 100

# Output CSV
CSV_FILE = "reddit_mental_health_posts.csv"

# Initialize headers
headers_written = False

with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as csvfile:
    writer = None
    offset = 0
    total_rows = 0

    while True:
        # Construct API URL
        url = f"{BASE_URL}?dataset={DATASET}&config={CONFIG}&split={SPLIT}&offset={offset}&length={CHUNK_SIZE}"

        print(f"Fetching: offset {offset}")
        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Failed to fetch: {response.status_code}")
            break

        data = response.json()
        rows = data.get("rows", [])

        if not rows:
            print("✅ All data fetched.")
            break

        for item in rows:
            record = item["row"]

            # Initialize CSV headers
            if not headers_written:
                writer = csv.DictWriter(csvfile, fieldnames=record.keys())
                writer.writeheader()
                headers_written = True

            writer.writerow(record)
            total_rows += 1

        offset += CHUNK_SIZE
        time.sleep(1)  # Optional sleep to be gentle on API

print(f"\n✅ Finished. Total records saved: {total_rows} → {CSV_FILE}")

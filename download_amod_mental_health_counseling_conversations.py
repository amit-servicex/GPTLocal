import requests
import csv
import time

# API Config
DATASET = "Amod/mental_health_counseling_conversations"
BASE_URL = "https://datasets-server.huggingface.co/rows"
CONFIG = "default"
SPLIT = "train"
CHUNK_SIZE = 100

# Output CSV
CSV_FILE = "amod_mental_health_counseling_conversations.csv"

# CSV writing setup
headers_written = False

with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as csvfile:
    writer = None
    offset = 0
    total_rows = 0

    while True:
        url = f"{BASE_URL}?dataset={DATASET}&config={CONFIG}&split={SPLIT}&offset={offset}&length={CHUNK_SIZE}"
        print(f"Fetching offset {offset}...")

        response = requests.get(url)

        if response.status_code != 200:
            print(f"❌ Error fetching data: HTTP {response.status_code}")
            break

        data = response.json()
        rows = data.get("rows", [])

        if not rows:
            print("✅ All records fetched.")
            break

        for item in rows:
            record = item["row"]

            # Initialize CSV writer with headers
            if not headers_written:
                writer = csv.DictWriter(csvfile, fieldnames=record.keys())
                writer.writeheader()
                headers_written = True

            writer.writerow(record)
            total_rows += 1

        offset += CHUNK_SIZE
        time.sleep(1)  # Be kind to the server

print(f"\n✅ Download complete. Total rows saved: {total_rows} → {CSV_FILE}")

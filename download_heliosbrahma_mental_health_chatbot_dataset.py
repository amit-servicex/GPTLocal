import requests
import csv
import time

# API config
DATASET = "heliosbrahma/mental_health_chatbot_dataset"
BASE_URL = "https://datasets-server.huggingface.co/rows"
CONFIG = "default"
SPLIT = "train"
CHUNK_SIZE = 100

# Output CSV
CSV_FILE = "helios_mental_health_chatbot_dataset.csv"

# Initialize CSV
headers_written = False

with open(CSV_FILE, mode="w", encoding="utf-8", newline="") as csvfile:
    writer = None
    offset = 0
    total_rows = 0

    while True:
        # Construct the paginated URL
        url = f"{BASE_URL}?dataset={DATASET}&config={CONFIG}&split={SPLIT}&offset={offset}&length={CHUNK_SIZE}"
        print(f"Fetching offset {offset}...")

        response = requests.get(url)
        if response.status_code != 200:
            print(f"❌ Error fetching data: HTTP {response.status_code}")
            break

        data = response.json()
        rows = data.get("rows", [])

        if not rows:
            print("✅ All data fetched.")
            break

        for item in rows:
            record = item["row"]

            if not headers_written:
                writer = csv.DictWriter(csvfile, fieldnames=record.keys())
                writer.writeheader()
                headers_written = True

            writer.writerow(record)
            total_rows += 1

        offset += CHUNK_SIZE
        time.sleep(1)  # Avoid rate limiting

print(f"\n✅ Completed. Total rows saved: {total_rows} → {CSV_FILE}")

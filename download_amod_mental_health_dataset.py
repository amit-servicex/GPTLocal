from datasets import load_dataset
import pandas as pd

# Load full dataset from Hugging Face
dataset = load_dataset("Amod/mental_health_counseling_conversations", split="train")

# Convert to Pandas DataFrame
df = pd.DataFrame(dataset)

# Save to CSV
output_file = "amod_mental_health_counseling_conversations.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"✅ Dataset saved to: {output_file}")

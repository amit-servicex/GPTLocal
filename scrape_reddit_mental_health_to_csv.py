import praw
import csv
import time
from datetime import datetime

# 🔐 Reddit API credentials
reddit = praw.Reddit(
    client_id="BjJl1Dp0w6nK3n5qdRx0fg",  # Replace with your client_id
    client_secret="22dsc0A_7miVud6W6UET1Xs-V2gmQA",  # Replace with your client_secret
    user_agent="mentalhealthscreener by u/CowNo7276"
)

# 🧠 Subreddits to scrape
subreddits = ["depression", "Anxiety", "mentalhealth", "OffMyChest"]

# 📁 CSV Output File
csv_file = "mental_health_reddit_data.csv"

# 🏷️ CSV Headers
headers = ["subreddit", "title", "selftext", "top_comments", "score", "created_utc", "permalink"]

# 🧾 Open file for writing
with open(csv_file, mode="w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=headers)
    writer.writeheader()

    print("Starting data collection...")

    for sub in subreddits:
        subreddit = reddit.subreddit(sub)
        print(f"\nFetching posts from r/{sub}...")

        for post in subreddit.top(limit=100):  # You can use .hot(), .new() too
            try:
                post.comments.replace_more(limit=0)
                top_comments = [c.body for c in post.comments[:5] if hasattr(c, "body")]
                top_comments_text = " ||| ".join(top_comments)

                writer.writerow({
                    "subreddit": sub,
                    "title": post.title,
                    "selftext": post.selftext,
                    "top_comments": top_comments_text,
                    "score": post.score,
                    "created_utc": datetime.utcfromtimestamp(post.created_utc).isoformat(),
                    "permalink": f"https://reddit.com{post.permalink}"
                })

                time.sleep(1)  # Be nice to Reddit servers
            except Exception as e:
                print(f"❌ Error fetching post: {e}")
                continue

print(f"\n✅ Data collection complete. Saved to '{csv_file}'")

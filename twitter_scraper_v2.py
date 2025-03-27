import tweepy
import os
from dotenv import load_dotenv
import csv
import re
import time

# Load credentials
load_dotenv(dotenv_path="/Users/danielmora/Interactly/.env")
bearer_token = os.getenv("BEARER_TOKEN")

# Confirm token exists
if not bearer_token:
    raise ValueError("❌ BEARER_TOKEN not found in .env")

# Init client
client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)

# Verify bearer token works
try:
    me = client.get_user(username="AmazonHelp")
    print("✅ Bearer token working. Sample user ID:", me.data.id)
except Exception as e:
    print("❌ Token failed:", e)
    exit()

# Limit query to one brand for now
query = "@AmazonHelp -is:retweet lang:en"

# Output CSV
output_file = "customer_tweets_v2.csv"
fields = ["tweet_id", "username", "text", "created_at"]

# Text cleaner
def clean_text(text):
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"#\w+", "", text)
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip().lower()

# Write CSV
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(fields)

    try:
        tweets = tweepy.Paginator(
            client.search_recent_tweets,
            query=query,
            tweet_fields=["created_at", "author_id", "text"],
            expansions=["author_id"],
            user_fields=["username"],
            max_results=100
        ).flatten(limit=50)  # Lowered for testing

        user_map = {}

        count = 0
        for tweet in tweets:
            user_id = tweet.author_id
            if user_id not in user_map:
                try:
                    user = client.get_user(id=user_id)
                    username = user.data.username
                    user_map[user_id] = username
                except Exception as e:
                    print(f"⚠️ Skipping user {user_id}: {e}")
                    continue
            else:
                username = user_map[user_id]

            cleaned = clean_text(tweet.text)
            print(f"📝 Fetched tweet: {cleaned[:80]}...")
            writer.writerow([tweet.id, username, cleaned, tweet.created_at])
            count += 1

        print(f"\n✅ Done. {count} tweets saved to {output_file}")

    except tweepy.TooManyRequests:
        print("⏳ Rate limit hit. Try again in 15 minutes.")
    except Exception as e:
        print("❌ Error during scraping:", e)

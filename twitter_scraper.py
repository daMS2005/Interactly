import tweepy
import os
from dotenv import load_dotenv
import csv
import re

# Load .env
load_dotenv(dotenv_path="/Users/danielmora/Interactly/.env")

# Load credentials
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

# Auth
auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

print(f"✅ Authenticated as: {api.verify_credentials().screen_name}")

# Target accounts
accounts = [
    "AmazonHelp", "Zara_Care", "ASOS_HeretoHelp", "WalmartHelp",
    "AskPayPal", "ChaseSupport", "AmericanExpress",
    "ATTHelp", "TMobileHelp", "VerizonSupport",
    "SpotifyCares", "AppleSupport", "Delta", "AskAirCanada", "HiltonHelp"
]

query = " OR ".join([f'@{acc}' for acc in accounts])

# Text cleaner
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # URLs
    text = re.sub(r"@\w+", "", text)     # Mentions
    text = re.sub(r"#\w+", "", text)     # Hashtags
    text = re.sub(r"[^\w\s]", "", text)  # Punctuation
    return text.strip().lower()

# Output CSV
output_file = "customer_tweets.csv"
fields = ["tweet_id", "username", "text", "created_at"]

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(fields)

    for tweet in tweepy.Cursor(api.search_tweets, q=query, lang="en", tweet_mode="extended").items(500):
        if hasattr(tweet, "retweeted_status"):
            text = tweet.retweeted_status.full_text
        else:
            text = tweet.full_text

        cleaned = clean_text(text)
        writer.writerow([tweet.id_str, tweet.user.screen_name, cleaned, tweet.created_at])

print(f"📁 Tweets saved to {output_file}")

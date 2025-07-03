import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# MongoDB configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "reddit_crawler")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "posts")

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "your_client_id")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "your_client_secret")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "fastapi-reddit-crawler")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "your_reddit_username")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "your_reddit_password")
REDDIT_CRAWL_INTERVAL_SECONDS = int(os.getenv("REDDIT_CRAWL_INTERVAL_SECONDS", 300))

# Hacker News API Configuration
HACKERNEWS_BASE_URL = "https://hacker-news.firebaseio.com/v0"
HACKERNEWS_FETCH_INTERVAL_SECONDS = int(os.getenv("HACKERNEWS_FETCH_INTERVAL_SECONDS", 60))

# YouTube API Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "your_youtube_api_key")
YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3"
YOUTUBE_FETCH_INTERVAL_SECONDS = int(os.getenv("YOUTUBE_FETCH_INTERVAL_SECONDS", 300))

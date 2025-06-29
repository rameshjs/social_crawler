
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "reddit_crawler")
MONGO_COLLECTION_NAME = os.getenv("MONGO_COLLECTION_NAME", "posts")

REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "your_client_id")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "your_client_secret")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "fastapi-reddit-crawler")
REDDIT_USERNAME = os.getenv("REDDIT_USERNAME", "your_reddit_username")
REDDIT_PASSWORD = os.getenv("REDDIT_PASSWORD", "your_reddit_password")
REDDIT_CRAWL_INTERVAL_SECONDS = int(os.getenv("REDDIT_CRAWL_INTERVAL_SECONDS", 300))

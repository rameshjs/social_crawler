import redis
import requests
from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import (
    REDIS_HOST,
    REDIS_PORT,
    MONGO_URI,
    MONGO_DB_NAME,
    HACKERNEWS_BASE_URL,
    HACKERNEWS_TTL_SECONDS,
)

# Constants for Redis keys and MongoDB collections
HACKERNEWS_POST_QUEUE_KEY = "hackernews:post_queue"
HACKERNEWS_LAST_FETCHED_KEY = "hackernews:last_fetched"
HACKERNEWS_COLLECTION_NAME = "hackernews_posts"

# Initialize Redis client for queue management
redis_client = redis.Redis(
    host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True
)

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
hackernews_collection = db[HACKERNEWS_COLLECTION_NAME]

# Create TTL index for Hacker News posts
try:
    hackernews_collection.create_index("created_at", expireAfterSeconds=HACKERNEWS_TTL_SECONDS)
    print(f"Created TTL index for Hacker News posts with {HACKERNEWS_TTL_SECONDS} seconds expiry")
except Exception as e:
    print(f"Error creating TTL index for Hacker News posts: {e}")


def get_latest_post_ids() -> List[int]:
    """Fetch latest post IDs from Hacker News API."""
    try:
        response = requests.get(f"{HACKERNEWS_BASE_URL}/newstories.json", timeout=10)
        response.raise_for_status()
        post_ids = response.json()[:10]
        print(f"Fetched {len(post_ids)} latest post IDs from Hacker News")
        return post_ids
    except requests.RequestException as e:
        print(f"Error fetching latest post IDs from Hacker News: {e}")
        return []


def get_last_fetched_post_id() -> Optional[int]:
    """Get the last fetched post ID from Redis."""
    last_id = redis_client.get(HACKERNEWS_LAST_FETCHED_KEY)
    return int(last_id) if last_id else None


def set_last_fetched_post_id(post_id: int) -> None:
    """Set the last fetched post ID in Redis."""
    redis_client.set(HACKERNEWS_LAST_FETCHED_KEY, post_id)


def add_post_to_queue(post_id: int) -> None:
    """Add a post ID to the processing queue."""
    redis_client.lpush(HACKERNEWS_POST_QUEUE_KEY, post_id)


def get_post_from_queue() -> Optional[int]:
    """Get a post ID from the processing queue (FIFO)."""
    post_id = redis_client.rpop(HACKERNEWS_POST_QUEUE_KEY)
    return int(post_id) if post_id else None


def fetch_post_data(post_id: int) -> Optional[Dict[str, Any]]:
    """Fetch individual post data from Hacker News API."""
    try:
        response = requests.get(f"{HACKERNEWS_BASE_URL}/item/{post_id}.json", timeout=10)
        response.raise_for_status()
        post_data = response.json()
        if post_data and post_data.get("type") == "story":
            return {
                "id": post_data.get("id"),
                "title": post_data.get("title", ""),
                "url": post_data.get("url", ""),
                "text": post_data.get("text", ""),
                "score": post_data.get("score", 0),
                "by": post_data.get("by", ""),
                "time": post_data.get("time"),
                "descendants": post_data.get("descendants", 0),
                "kids": post_data.get("kids", []),
                "type": post_data.get("type"),
                "created_at": datetime.fromtimestamp(post_data.get("time", 0)),
                "fetched_at": datetime.now(),
            }
        return None
    except requests.RequestException as e:
        print(f"Error fetching post {post_id} from Hacker News: {e}")
        return None


def save_post_to_mongodb(post_data: Dict[str, Any]) -> bool:
    """Save post data to MongoDB."""
    try:
        existing_post = hackernews_collection.find_one({"id": post_data["id"]})
        if existing_post:
            print(f"Post {post_data['id']} already exists, skipping...")
            return True
        
        result = hackernews_collection.insert_one(post_data)
        print(f"Saved Hacker News post {post_data['id']} to MongoDB")
        return True
        
    except Exception as e:
        print(f"Error saving post {post_data['id']} to MongoDB: {e}")
        return False


def fetch_latest_posts() -> None:
    """Fetch latest post IDs and add them to the processing queue."""
    print("Fetching latest Hacker News posts...")
    
    latest_post_ids = get_latest_post_ids()
    if not latest_post_ids:
        print("No latest posts found")
        return
    
    last_fetched_id = get_last_fetched_post_id()
    
    new_post_ids = []
    for post_id in latest_post_ids:
        if not last_fetched_id or post_id > last_fetched_id:
            new_post_ids.append(post_id)
    
    if not new_post_ids:
        print("No new posts to process")
        return
    
    for post_id in new_post_ids:
        add_post_to_queue(post_id)
    
    set_last_fetched_post_id(max(new_post_ids))
    
    print(f"Added {len(new_post_ids)} new posts to processing queue")


def process_post_queue() -> None:
    """Process posts from the queue and save them to MongoDB."""
    print("Processing Hacker News post queue...")
    
    processed_count = 0
    max_posts_per_run = 5
    
    for _ in range(max_posts_per_run):
        post_id = get_post_from_queue()
        if not post_id:
            print("No posts in queue to process")
            break
        
        post_data = fetch_post_data(post_id)
        if not post_data:
            print(f"Failed to fetch data for post {post_id}")
            continue
        
        if save_post_to_mongodb(post_data):
            processed_count += 1
            print(f"Successfully processed post {post_id}")
    
    if processed_count > 0:
        print(f"Processed {processed_count} posts from queue")
    else:
        print("No posts processed from queue") 
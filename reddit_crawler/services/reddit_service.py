import requests
import redis
from pymongo import MongoClient
from config import REDIS_HOST, REDIS_PORT, MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

LAST_POST_ID_KEY = "last_post_id"

def get_last_post_id():
    return redis_client.get(LAST_POST_ID_KEY)

def set_last_post_id(post_id):
    redis_client.set(LAST_POST_ID_KEY, post_id)

def fetch_new_reddit_posts():
    last_post_id = get_last_post_id()
    headers = {"User-Agent": "fastapi-reddit-crawler"}
    url = "https://www.reddit.com/r/all/new.json?limit=10"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        posts = response.json()["data"]["children"]

        new_posts = []
        for post in posts:
            post_data = post["data"]
            if post_data["id"] == last_post_id:
                break
            new_posts.append({
                "id": post_data["id"],
                "title": post_data["title"],
                "url": post_data["url"],
                "description": post_data["selftext"],
                "created_utc": post_data["created_utc"]
            })

        if new_posts:
            collection.insert_many(list(reversed(new_posts)))
            set_last_post_id(new_posts[0]["id"])

        print(f"Fetched {len(new_posts)} new posts")

    except Exception as e:
        print(f"Error fetching posts: {e}")

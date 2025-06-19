import json
import os
import requests

DATA_DIR = "data"
POSTS_FILE = os.path.join(DATA_DIR, "reddit_posts.json")
LAST_ID_FILE = os.path.join(DATA_DIR, "last_post_id.txt")

os.makedirs(DATA_DIR, exist_ok=True)

def get_last_post_id():
    if os.path.exists(LAST_ID_FILE):
        with open(LAST_ID_FILE, "r") as f:
            return f.read().strip()
    return None

def set_last_post_id(post_id):
    with open(LAST_ID_FILE, "w") as f:
        f.write(post_id)

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
                "created_utc": post_data["created_utc"]
            })

        if new_posts:
            with open(POSTS_FILE, "a") as f:
                for p in reversed(new_posts):
                    f.write(json.dumps(p) + "\n")
            set_last_post_id(new_posts[0]["id"])

        print(f"Fetched {len(new_posts)} new posts")

    except Exception as e:
        print(f"Error fetching posts: {e}")

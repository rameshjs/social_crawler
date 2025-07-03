import requests
from pymongo import MongoClient
from datetime import datetime
from typing import List, Dict, Any, Optional
from config import (
    MONGO_URI,
    MONGO_DB_NAME,
    YOUTUBE_API_KEY,
    YOUTUBE_BASE_URL,
)

# Constants for MongoDB collections
YOUTUBE_TRENDING_COLLECTION_NAME = "youtube_trending_videos"

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
trending_collection = db[YOUTUBE_TRENDING_COLLECTION_NAME]


def fetch_trending_videos_api() -> List[Dict[str, Any]]:
    """Fetch trending videos from YouTube Data API."""
    try:
        url = f"{YOUTUBE_BASE_URL}/videos"
        params = {
            "part": "snippet,statistics",
            "chart": "mostPopular",
            "regionCode": "US",
            "maxResults": 50,
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if "items" in data:
            videos = data["items"]
            print(f"Fetched {len(videos)} trending videos from YouTube")
            return videos
        
        return []
        
    except requests.RequestException as e:
        print(f"Error fetching trending videos from YouTube: {e}")
        return []


def save_video_to_mongodb(video_data: Dict[str, Any]) -> bool:
    """Save video data to MongoDB."""
    try:
        video_id = video_data["id"]
        
        # Check if video already exists
        existing_video = trending_collection.find_one({"videoId": video_id})
        if existing_video:
            print(f"Video {video_id} already exists, skipping...")
            return True
        
        # Extract relevant data
        snippet = video_data.get("snippet", {})
        statistics = video_data.get("statistics", {})
        
        video_doc = {
            "videoId": video_id,
            "title": snippet.get("title", ""),
            "description": snippet.get("description", ""),
            "publishedAt": snippet.get("publishedAt"),
            "channelTitle": snippet.get("channelTitle", ""),
            "channelId": snippet.get("channelId", ""),
            "viewCount": int(statistics.get("viewCount", 0)),
            "likeCount": int(statistics.get("likeCount", 0)),
            "commentCount": int(statistics.get("commentCount", 0)),
            "tags": snippet.get("tags", []),
            "categoryId": snippet.get("categoryId", ""),
            "fetched_at": datetime.now(),
        }
        
        result = trending_collection.insert_one(video_doc)
        print(f"Saved YouTube trending video {video_id} to MongoDB")
        return True
        
    except Exception as e:
        print(f"Error saving video {video_data.get('id', 'unknown')} to MongoDB: {e}")
        return False


def fetch_trending_videos() -> None:
    """Fetch trending videos and save them to MongoDB."""
    print("Fetching YouTube trending videos...")
    
    videos = fetch_trending_videos_api()
    if not videos:
        print("No trending videos found")
        return
    
    saved_count = 0
    for video in videos:
        if save_video_to_mongodb(video):
            saved_count += 1
    
    print(f"Successfully saved {saved_count} new trending videos to MongoDB") 
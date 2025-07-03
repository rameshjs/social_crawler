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
YOUTUBE_COMMENTS_COLLECTION_NAME = "youtube_latest_comments"

# Initialize MongoDB client
mongo_client = MongoClient(MONGO_URI)
db = mongo_client[MONGO_DB_NAME]
comments_collection = db[YOUTUBE_COMMENTS_COLLECTION_NAME]


def get_popular_video_ids() -> List[str]:
    """Get a list of popular video IDs to fetch comments from."""
    try:
        # Get recent trending videos from our database
        recent_videos = list(db.youtube_trending_videos.find(
            {}, 
            {"videoId": 1}
        ).sort("fetched_at", -1).limit(10))
        
        video_ids = [video["videoId"] for video in recent_videos]
        
        # Fallback: use some known popular video IDs if no trending videos found
        if not video_ids:
            fallback_ids = [
                "dQw4w9WgXcQ",  # Rick Roll
                "kJQP7kiw5Fk",  # Despacito
                "9bZkp7q19f0",  # Gangnam Style
                "ZZ5LpwO-An4",  # Baby Shark
                "kJQP7kiw5Fk",  # Despacito
            ]
            video_ids = fallback_ids
        
        return video_ids
        
    except Exception as e:
        print(f"Error getting popular video IDs: {e}")
        return []


def fetch_comments_for_video(video_id: str) -> List[Dict[str, Any]]:
    """Fetch comments for a specific video."""
    try:
        url = f"{YOUTUBE_BASE_URL}/commentThreads"
        params = {
            "part": "snippet",
            "videoId": video_id,
            "maxResults": 100,
            "order": "time",  # Get latest comments first
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if "items" in data:
            comments = data["items"]
            print(f"Fetched {len(comments)} comments for video {video_id}")
            return comments
        
        return []
        
    except requests.RequestException as e:
        print(f"Error fetching comments for video {video_id}: {e}")
        return []


def save_comment_to_mongodb(comment_data: Dict[str, Any]) -> bool:
    """Save comment data to MongoDB."""
    try:
        comment_id = comment_data["id"]
        
        # Check if comment already exists
        existing_comment = comments_collection.find_one({"commentId": comment_id})
        if existing_comment:
            print(f"Comment {comment_id} already exists, skipping...")
            return True
        
        # Extract relevant data
        snippet = comment_data.get("snippet", {})
        top_level_comment = snippet.get("topLevelComment", {}).get("snippet", {})
        
        comment_doc = {
            "commentId": comment_id,
            "videoId": snippet.get("videoId", ""),
            "author": top_level_comment.get("authorDisplayName", ""),
            "authorChannelId": top_level_comment.get("authorChannelId", {}).get("value", ""),
            "text": top_level_comment.get("textDisplay", ""),
            "publishedAt": top_level_comment.get("publishedAt"),
            "updatedAt": top_level_comment.get("updatedAt"),
            "likeCount": int(top_level_comment.get("likeCount", 0)),
            "totalReplyCount": int(snippet.get("totalReplyCount", 0)),
            "fetched_at": datetime.now(),
        }
        
        result = comments_collection.insert_one(comment_doc)
        print(f"Saved YouTube comment {comment_id} to MongoDB")
        return True
        
    except Exception as e:
        print(f"Error saving comment {comment_data.get('id', 'unknown')} to MongoDB: {e}")
        return False


def fetch_latest_comments() -> None:
    """Fetch latest comments from popular videos and save them to MongoDB."""
    print("Fetching YouTube latest comments...")
    
    video_ids = get_popular_video_ids()
    if not video_ids:
        print("No video IDs found to fetch comments from")
        return
    
    total_saved = 0
    
    for video_id in video_ids[:5]:  # Limit to 5 videos to avoid API quota issues
        print(f"Fetching comments for video: {video_id}")
        comments = fetch_comments_for_video(video_id)
        
        if not comments:
            continue
        
        saved_count = 0
        for comment in comments:
            if save_comment_to_mongodb(comment):
                saved_count += 1
        
        total_saved += saved_count
        print(f"Saved {saved_count} new comments for video {video_id}")
    
    print(f"Successfully saved {total_saved} new comments to MongoDB") 
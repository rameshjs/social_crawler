#!/usr/bin/env python3
"""
Test script for YouTube integration
"""

from youtube_crawler.services.youtube_trending_service import (
    fetch_trending_videos,
    fetch_trending_videos_api
)
from youtube_crawler.services.youtube_comment_service import (
    fetch_latest_comments,
    get_popular_video_ids,
    fetch_comments_for_video
)
from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME, YOUTUBE_API_KEY

def test_youtube_integration():
    print("=== Testing YouTube Integration ===\n")
    
    # Test 1: Check API key
    print("1. Checking YouTube API key...")
    if YOUTUBE_API_KEY == "your_youtube_api_key":
        print("   ⚠️  Please set YOUTUBE_API_KEY in your environment")
        print("   Skipping API tests...")
        return
    else:
        print("   ✅ YouTube API key is configured")
    
    # Test 2: Test trending videos API
    print("\n2. Testing trending videos API...")
    try:
        videos = fetch_trending_videos_api()
        if videos:
            print(f"   ✅ Successfully fetched {len(videos)} trending videos")
            print(f"   Sample video: {videos[0].get('snippet', {}).get('title', 'N/A')[:50]}...")
        else:
            print("   ❌ No trending videos fetched")
    except Exception as e:
        print(f"   ❌ Error fetching trending videos: {e}")
    
    # Test 3: Test MongoDB connection
    print("\n3. Testing MongoDB connection...")
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        trending_collection = db['youtube_trending_videos']
        comments_collection = db['youtube_latest_comments']
        
        trending_count = trending_collection.count_documents({})
        comments_count = comments_collection.count_documents({})
        
        print(f"   ✅ MongoDB connected successfully")
        print(f"   Current trending videos: {trending_count}")
        print(f"   Current comments: {comments_count}")
    except Exception as e:
        print(f"   ❌ MongoDB connection failed: {e}")
        return
    
    # Test 4: Test trending videos workflow
    print("\n4. Testing trending videos workflow...")
    try:
        fetch_trending_videos()
        new_trending_count = trending_collection.count_documents({})
        print(f"   ✅ Trending videos workflow completed")
        print(f"   New total trending videos: {new_trending_count}")
    except Exception as e:
        print(f"   ❌ Trending videos workflow failed: {e}")
    
    # Test 5: Test comments workflow
    print("\n5. Testing comments workflow...")
    try:
        fetch_latest_comments()
        new_comments_count = comments_collection.count_documents({})
        print(f"   ✅ Comments workflow completed")
        print(f"   New total comments: {new_comments_count}")
    except Exception as e:
        print(f"   ❌ Comments workflow failed: {e}")
    
    # Test 6: Show sample data
    print("\n6. Sample data from MongoDB:")
    try:
        # Show latest trending video
        latest_video = trending_collection.find_one(
            {}, 
            {"videoId": 1, "title": 1, "channelTitle": 1, "viewCount": 1}
        )
        if latest_video:
            print(f"   Latest trending video: {latest_video['title'][:60]}...")
            print(f"   Channel: {latest_video['channelTitle']}, Views: {latest_video['viewCount']}")
        
        # Show latest comment
        latest_comment = comments_collection.find_one(
            {}, 
            {"commentId": 1, "author": 1, "text": 1, "videoId": 1}
        )
        if latest_comment:
            print(f"   Latest comment by {latest_comment['author']}: {latest_comment['text'][:50]}...")
    except Exception as e:
        print(f"   ❌ Error showing sample data: {e}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_youtube_integration() 
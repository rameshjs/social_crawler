#!/usr/bin/env python3
"""
Test script for Hacker News integration
"""

from hackernews_crawler.services.hackernews_service import (
    fetch_latest_posts, 
    process_post_queue,
    get_latest_post_ids,
    fetch_post_data,
    save_post_to_mongodb
)
from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME
import redis
from config import REDIS_HOST, REDIS_PORT

def test_hackernews_integration():
    print("=== Testing Hacker News Integration ===\n")
    
    # Test 1: Fetch latest post IDs
    print("1. Testing API connection...")
    post_ids = get_latest_post_ids()
    print(f"   Fetched {len(post_ids)} post IDs: {post_ids[:3]}...")
    
    # Test 2: Fetch individual post data
    print("\n2. Testing individual post fetch...")
    if post_ids:
        post_data = fetch_post_data(post_ids[0])
        if post_data:
            print(f"   Successfully fetched post {post_data['id']}: {post_data['title'][:50]}...")
        else:
            print("   Failed to fetch post data")
    
    # Test 3: Test MongoDB connection
    print("\n3. Testing MongoDB connection...")
    try:
        client = MongoClient(MONGO_URI)
        db = client[MONGO_DB_NAME]
        collection = db['hackernews_posts']
        count_before = collection.count_documents({})
        print(f"   Current posts in MongoDB: {count_before}")
    except Exception as e:
        print(f"   MongoDB connection failed: {e}")
        return
    
    # Test 4: Test Redis connection
    print("\n4. Testing Redis connection...")
    try:
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
        redis_client.ping()
        print("   Redis connection successful")
    except Exception as e:
        print(f"   Redis connection failed: {e}")
        return
    
    # Test 5: Test full workflow
    print("\n5. Testing full workflow...")
    fetch_latest_posts()
    process_post_queue()
    
    # Test 6: Verify data was saved
    print("\n6. Verifying data was saved...")
    count_after = collection.count_documents({})
    print(f"   Posts in MongoDB after test: {count_after}")
    print(f"   New posts added: {count_after - count_before}")
    
    # Show latest posts
    latest_posts = list(collection.find({}, {'id': 1, 'title': 1, 'by': 1}).sort('fetched_at', -1).limit(3))
    print("\n   Latest 3 posts:")
    for post in latest_posts:
        print(f"   - ID: {post['id']}, Title: {post['title'][:60]}..., Author: {post['by']}")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_hackernews_integration() 
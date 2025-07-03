YouTube Integration ✅ COMPLETED

Description:
Fetch globally trending YouTube videos and globally recent public comments. Store video and comment data in separate MongoDB collections. Two independent services: one for trending videos, one for latest comments.

Requirements:

Use YouTube Data API to fetch:

chart=mostPopular for globally trending videos

commentThreads.list with search or known workaround to get globally recent public comments

Save video metadata (title, description, videoId, publish time) to a MongoDB collection.

Save comment data (comment text, author, published time, videoId, etc.) to a separate MongoDB collection.

No queueing needed — fetch latest, deduplicate, and store.

Implementation Details:

Created youtube_crawler/ package with two independent services.

Job 1: fetch_trending_videos()

Fetches from videos.list?chart=mostPopular&regionCode=US

Fields: videoId, title, description, publishedAt, channelTitle, viewCount, likeCount, commentCount

Saves to MongoDB collection: youtube_trending_videos

Deduplicates on videoId

Job 2: fetch_latest_comments()

Uses commentThreads.list via popular video IDs from trending videos

Fields: commentId, videoId, author, text, publishedAt, likeCount, totalReplyCount

Saves to MongoDB collection: youtube_latest_comments

Deduplicates on commentId

Scheduled jobs: Every 5 minutes (300 seconds)

Uses fallback popular video IDs if no trending videos found

Files Created/Modified:

youtube_crawler/__init__.py - Package initialization

youtube_crawler/youtube_crawler.py - Job definitions and task functions

youtube_crawler/services/__init__.py - Services package

youtube_crawler/services/youtube_trending_service.py - Trending videos service

youtube_crawler/services/youtube_comment_service.py - Comments service

config.py - Added YouTube API key and fetch limits

main.py - Registered YouTube jobs in scheduler

env.sample - Added YOUTUBE_API_KEY

test_youtube.py - Unit test and integration test coverage

MongoDB Collections:

youtube_trending_videos

youtube_latest_comments

Avoid these

Do not filter by specific channel or region unless required later.

Do not fetch video streams or media files.

Rules To Follow Before Starting the Project

Follow .cursor and service patterns used in Hacker News integration.

Break into two clear jobs: trending videos + latest comments


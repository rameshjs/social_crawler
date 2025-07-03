# Project Task Instructions

This file is for writing detailed tasks or requests for the AI to perform. Please use the following layout for best results:

---

## Hacker News Integration ✅ COMPLETED

**Description:**
Fetch latest hacker news posts and save them in mongodb, Two services one for fetching the posts latest and other to fetch indivigual post data in another service and removes them from queue.

**Requirements:**
- Use hacker news api to feth latest posts
- It returns latest post id so save the post id in a redis and let a job fetch indivigua lpost id fetch the post data and remove it from queue.
- So in  short two service one to fetch list of latest post if and other to fetch indivigual post data from those saved post id and removes them on successful fetch.
- Then save the data to mongodb in a structured way.

**Implementation Details:**
- Created `hackernews_crawler/` package with service architecture
- **Service 1**: `fetch_latest_posts()` - Fetches latest post IDs from Hacker News API and adds to Redis queue
- **Service 2**: `process_post_queue()` - Processes post IDs from queue, fetches individual post data, and saves to MongoDB
- Uses Redis for queue management with keys: `hackernews:post_queue` and `hackernews:last_fetched`
- MongoDB collection: `hackernews_posts` for storing structured post data
- Scheduled jobs: Fetch every 60 seconds, Process every 30 seconds
- Follows existing codebase patterns and cursor rules

**Files Created/Modified:**
- `hackernews_crawler/__init__.py` - Package initialization
- `hackernews_crawler/hackernews_crawler.py` - Job definitions and task functions
- `hackernews_crawler/services/__init__.py` - Services package
- `hackernews_crawler/services/hackernews_service.py` - Core service logic
- `config.py` - Added Hacker News configuration constants
- `main.py` - Added Hacker News jobs to scheduler
- `env.sample` - Added Hacker News environment variables
- `test_hackernews.py` - Test script for integration

**Avoid these**
- Dont create things thats not described in task on your own.
- Dont remove any other sections of code if its not relevant to the task.

**Rules To follow before starting the project**
- check the .cursor rules and existing code base before you start the work.
- Break down the project to smaller scopes and track and acheive those.

---

# Project Task Instructions

This file is for writing detailed tasks or requests for the AI to perform. Please use the following layout for best results:

---

## Auto expiring documents ✅ COMPLETED

**Description:**
Each documents in collection will expiry after the specificed interval specified in .env file, Take advantage of mongodb inbuilt ttl.

**Requirements:**
- Reads .env and when adding each document make it ttl.
- I can have different interval for each crawler.

**Implementation:**
- Added TTL configuration variables to env.sample and config.py
- Created TTL indexes for all collections:
  - Reddit posts: 24 hours (86400 seconds)
  - Hacker News posts: 7 days (604800 seconds)  
  - YouTube trending videos: 24 hours (86400 seconds)
  - YouTube comments: 7 days (604800 seconds)
- Each service now creates TTL index on startup using MongoDB's `expireAfterSeconds`
- Documents automatically expire based on `created_at` or `fetched_at` timestamps

**Avoid these**
- Dont create things thats not described in task on your own.
- Dont remove any other sections of code if its not relevant to the task.

**Rules To follow before starting the project**
- check the .cursor rules and existing code base before you start the work.
- Break down the project to smaller scopes and track and acheive those.

---

# Project Task Instructions

This file is for writing detailed tasks or requests for the AI to perform. Please use the following layout for best results:

---

## Hacker rank integration

**Description:**
Fetch latest hacker rank posts and save them in mongidb, Two services one for fetching the posts latest and other to fetch indivigual post data in another service and removes them from queue.

**Requirements:**
- Use hacker rank api to feth latest posts
- It returns latest post id so save the post id in a redis and let a job fetch indivigua lpost id fetch the post data and remove it from queue.
- So in  short two service one to fetch list of latest post if and other to fetch indivigual post data from those saved post id and removes them on successful fetch.
- Then save the data to mongodb in a structured way.

**Rules**
check the .cursor rules and existing code base before you start the work.

---

from apscheduler.triggers.interval import IntervalTrigger
from scheduler import scheduler
from reddit_crawler.services.reddit_service import fetch_new_reddit_posts

# Unique job ID for Reddit crawler
REDDIT_JOB_ID = "reddit-crawler-job"

def reddit_crawl_task():
    print("Starting Reddit crawl task...")
    fetch_new_reddit_posts()

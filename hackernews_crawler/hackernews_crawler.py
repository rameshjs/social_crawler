from apscheduler.triggers.interval import IntervalTrigger
from scheduler import scheduler
from hackernews_crawler.services.hackernews_service import fetch_latest_posts, process_post_queue

# Constants for job configuration
HACKERNEWS_FETCH_JOB_ID = "hackernews-fetch-job"
HACKERNEWS_PROCESS_JOB_ID = "hackernews-process-job"


def hackernews_fetch_task():
    """Execute the Hacker News fetch task to get latest post IDs."""
    print("Starting Hacker News fetch task...")
    fetch_latest_posts()


def hackernews_process_task():
    """Execute the Hacker News process task to fetch individual post data."""
    print("Starting Hacker News process task...")
    process_post_queue() 
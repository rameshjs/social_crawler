from apscheduler.triggers.interval import IntervalTrigger
from scheduler import scheduler
from reddit_crawler.services.reddit_service import fetch_new_reddit_posts

# Constants for job configuration
REDDIT_JOB_ID: str = "reddit-crawler-job"


def reddit_crawl_task() -> None:
    """Execute the Reddit crawling task."""
    print("Starting Reddit crawl task...")
    fetch_new_reddit_posts()

from apscheduler.triggers.interval import IntervalTrigger
from scheduler import scheduler
from youtube_crawler.services.youtube_trending_service import fetch_trending_videos
from youtube_crawler.services.youtube_comment_service import fetch_latest_comments

# Constants for job configuration
YOUTUBE_TRENDING_JOB_ID = "youtube-trending-job"
YOUTUBE_COMMENTS_JOB_ID = "youtube-comments-job"


def youtube_trending_task():
    """Execute the YouTube trending videos task."""
    print("Starting YouTube trending videos task...")
    fetch_trending_videos()


def youtube_comments_task():
    """Execute the YouTube latest comments task."""
    print("Starting YouTube latest comments task...")
    fetch_latest_comments() 
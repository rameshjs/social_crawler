from fastapi import FastAPI
from contextlib import asynccontextmanager
from scheduler import scheduler
from reddit_crawler.reddit_crawler import reddit_crawl_task, REDDIT_JOB_ID
from hackernews_crawler.hackernews_crawler import (
    hackernews_fetch_task, 
    hackernews_process_task, 
    HACKERNEWS_FETCH_JOB_ID, 
    HACKERNEWS_PROCESS_JOB_ID
)
from youtube_crawler.youtube_crawler import (
    youtube_trending_task,
    youtube_comments_task,
    YOUTUBE_TRENDING_JOB_ID,
    YOUTUBE_COMMENTS_JOB_ID
)
from apscheduler.triggers.interval import IntervalTrigger
from config import (
    REDDIT_CRAWL_INTERVAL_SECONDS, 
    HACKERNEWS_FETCH_INTERVAL_SECONDS,
    YOUTUBE_FETCH_INTERVAL_SECONDS
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for startup and shutdown."""
    try:
        scheduler.start()
        print("Scheduler started successfully.")

        # Schedule the Reddit crawler job
        scheduler.add_job(
            func=reddit_crawl_task,
            trigger=IntervalTrigger(seconds=REDDIT_CRAWL_INTERVAL_SECONDS),
            id=REDDIT_JOB_ID,
            replace_existing=True,
            misfire_grace_time=30,
        )
        print(
            f"Reddit crawler job scheduled to run every {REDDIT_CRAWL_INTERVAL_SECONDS} seconds."
        )

        # Schedule the Hacker News fetch job
        scheduler.add_job(
            func=hackernews_fetch_task,
            trigger=IntervalTrigger(seconds=HACKERNEWS_FETCH_INTERVAL_SECONDS),
            id=HACKERNEWS_FETCH_JOB_ID,
            replace_existing=True,
            misfire_grace_time=30,
        )
        print(
            f"Hacker News fetch job scheduled to run every {HACKERNEWS_FETCH_INTERVAL_SECONDS} seconds."
        )

        # Schedule the Hacker News process job (runs more frequently)
        scheduler.add_job(
            func=hackernews_process_task,
            trigger=IntervalTrigger(seconds=30),  # Process every 30 seconds
            id=HACKERNEWS_PROCESS_JOB_ID,
            replace_existing=True,
            misfire_grace_time=30,
        )
        print("Hacker News process job scheduled to run every 30 seconds.")

        # Schedule the YouTube trending videos job
        scheduler.add_job(
            func=youtube_trending_task,
            trigger=IntervalTrigger(seconds=YOUTUBE_FETCH_INTERVAL_SECONDS),
            id=YOUTUBE_TRENDING_JOB_ID,
            replace_existing=True,
            misfire_grace_time=30,
        )
        print(
            f"YouTube trending videos job scheduled to run every {YOUTUBE_FETCH_INTERVAL_SECONDS} seconds."
        )

        # Schedule the YouTube comments job
        scheduler.add_job(
            func=youtube_comments_task,
            trigger=IntervalTrigger(seconds=YOUTUBE_FETCH_INTERVAL_SECONDS),
            id=YOUTUBE_COMMENTS_JOB_ID,
            replace_existing=True,
            misfire_grace_time=30,
        )
        print(
            f"YouTube comments job scheduled to run every {YOUTUBE_FETCH_INTERVAL_SECONDS} seconds."
        )

        yield

    except Exception as e:
        print(f"Error during application startup: {e}")
        raise
    finally:
        # Shut down the scheduler and remove the jobs
        try:
            scheduler.remove_job(REDDIT_JOB_ID)
            scheduler.remove_job(HACKERNEWS_FETCH_JOB_ID)
            scheduler.remove_job(HACKERNEWS_PROCESS_JOB_ID)
            scheduler.remove_job(YOUTUBE_TRENDING_JOB_ID)
            scheduler.remove_job(YOUTUBE_COMMENTS_JOB_ID)
            scheduler.shutdown()
            print("Scheduler shut down successfully.")
        except Exception as e:
            print(f"Error during scheduler shutdown: {e}")


app = FastAPI(
    title="Social Crawler API",
    description="A FastAPI application for crawling Reddit, Hacker News, and YouTube posts and comments",
    version="1.0.0",
    lifespan=lifespan
)

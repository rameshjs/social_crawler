from fastapi import FastAPI
from contextlib import asynccontextmanager
from scheduler import scheduler
from reddit_crawler.reddit_crawler import reddit_crawl_task, REDDIT_JOB_ID
from apscheduler.triggers.interval import IntervalTrigger
from config import REDDIT_CRAWL_INTERVAL_SECONDS


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

        yield

    except Exception as e:
        print(f"Error during application startup: {e}")
        raise
    finally:
        # Shut down the scheduler and remove the job
        try:
            scheduler.remove_job(REDDIT_JOB_ID)
            scheduler.shutdown()
            print("Scheduler shut down successfully.")
        except Exception as e:
            print(f"Error during scheduler shutdown: {e}")


app = FastAPI(
    title="Social Crawler API",
    description="A FastAPI application for crawling Reddit posts and comments",
    version="1.0.0",
    lifespan=lifespan
)

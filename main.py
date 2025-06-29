from fastapi import FastAPI
from contextlib import asynccontextmanager
from scheduler import scheduler
from reddit_crawler.reddit_crawler import reddit_crawl_task, REDDIT_JOB_ID
from apscheduler.triggers.interval import IntervalTrigger
from config import REDDIT_CRAWL_INTERVAL_SECONDS


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    print("Scheduler started.")

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

    # Shut down the scheduler and remove the job
    scheduler.remove_job(REDDIT_JOB_ID)
    scheduler.shutdown()
    print("Scheduler shut down.")


app = FastAPI(lifespan=lifespan)

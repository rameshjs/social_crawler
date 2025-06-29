from fastapi import APIRouter, HTTPException
from apscheduler.triggers.interval import IntervalTrigger
from scheduler import scheduler
from reddit_crawler.services.reddit_service import fetch_new_reddit_posts

router = APIRouter()

# Unique job ID for Reddit crawler
REDDIT_JOB_ID = "reddit-crawler-job"

def reddit_crawl_task():
    print("Starting Reddit crawl task...")
    fetch_new_reddit_posts()

@router.post("/start-reddit-job/")
def start_reddit_job(delay: float):
    existing_job = scheduler.get_job(REDDIT_JOB_ID)
    if existing_job:
        raise HTTPException(status_code=400, detail="Reddit job already running")

    scheduler.add_job(
        func=reddit_crawl_task,
        trigger=IntervalTrigger(seconds=delay),
        id=REDDIT_JOB_ID,
        replace_existing=True,
        misfire_grace_time=30,
    )
    return {"message": "Reddit job started", "job_id": REDDIT_JOB_ID}

@router.post("/stop-reddit-job/")
def stop_reddit_job():
    job = scheduler.get_job(REDDIT_JOB_ID)
    if not job:
        raise HTTPException(status_code=404, detail="Reddit job not found")
    scheduler.remove_job(REDDIT_JOB_ID)
    return {"message": "Reddit job stopped"}

@router.get("/reddit-jobs")
def list_reddit_jobs():
    job = scheduler.get_job(REDDIT_JOB_ID)
    if not job:
        return {"job": None}
    return {"job_id": job.id, "next_run_time": job.next_run_time.isoformat()}
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from config import REDIS_HOST, REDIS_PORT

jobstores = {
    "default": RedisJobStore(
        jobs_key="apscheduler.jobs",
        run_times_key="apscheduler.run_times",
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=0
    )
}

scheduler = AsyncIOScheduler(jobstores=jobstores)

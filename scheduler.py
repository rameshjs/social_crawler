from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from config import REDIS_HOST, REDIS_PORT

# Constants for Redis job store configuration
REDIS_JOBS_KEY: str = "apscheduler.jobs"
REDIS_RUN_TIMES_KEY: str = "apscheduler.run_times"
REDIS_DB: int = 0

jobstores = {
    "default": RedisJobStore(
        jobs_key=REDIS_JOBS_KEY,
        run_times_key=REDIS_RUN_TIMES_KEY,
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB
    )
}

scheduler = AsyncIOScheduler(jobstores=jobstores)

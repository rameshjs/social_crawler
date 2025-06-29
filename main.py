from fastapi import FastAPI
from contextlib import asynccontextmanager
from scheduler import scheduler
from reddit_crawler.reddit_crawler import router as reddit_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    print("Scheduler started.")
    yield
    scheduler.shutdown()
    print("Scheduler shut down.")

app = FastAPI(lifespan=lifespan)

app.include_router(reddit_router, prefix="/api")
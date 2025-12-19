# app/main.py

import asyncio
import logging
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from app.api.health import router as health_router
from app.config import settings
from app.db.database import SessionLocal
from app.db.models import Base
from app.db.database import engine
from app.scheduler.jobs import scrape_and_publish
from app.utils.logging import setup_logging

log = logging.getLogger(__name__)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


scheduler: AsyncIOScheduler | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    init_db()

    global scheduler
    scheduler = AsyncIOScheduler()

    async def job_wrapper():
        db = SessionLocal()
        try:
            await scrape_and_publish(db)
        finally:
            db.close()

    scheduler.add_job(
        lambda: asyncio.create_task(job_wrapper()),
        trigger="interval",
        seconds=settings.scrape_interval_seconds,
        id="scrape_and_publish",
        replace_existing=True,
    )
    scheduler.start()
    log.info("Scheduler started (interval=%ss)", settings.scrape_interval_seconds)

    yield

    if scheduler:
        scheduler.shutdown(wait=False)
        log.info("Scheduler stopped")


app = FastAPI(title="Reality Telegram Bot API", lifespan=lifespan)
app.include_router(health_router)

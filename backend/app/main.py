from fastapi import FastAPI
from app.database import engine, Base
from contextlib import asynccontextmanager
from app.routers import teams
from app.services.scheduler import sync_la_liga_data
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s  - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sync_la_liga_data, 'interval', hours=6)
    scheduler.start()
    logger.info("Scheduler started for syncing La Liga teams every 6 hours.")

    yield
    scheduler.shutdown()
    logger.info("Scheduler shut down gracefully.")

app = FastAPI(
    title="La Liga Statistics API",
    description="Backend API for La Liga Statistics dashboard",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(teams.router)

@app.get("/")
def root():
    logger.info("Root endpoint accessed.")
    return {"status": "ok", "message": "La Liga API is running"}
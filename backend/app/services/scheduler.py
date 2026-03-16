from app.database import SessionLocal
from app.services.football_api import sync_teams
import logging

logger = logging.getLogger(__name__)

async def sync_la_liga_data():
    logger.info("Scheduled Sync Started: Updating La Liga Teams...")

    db = SessionLocal()
    try:
        await sync_teams(db=db, league_id=140)
        logger.info("Scheduled sync completed successfully.")
    except Exception as e:
        logger.error(f"Sync failed: {e}")
    finally:
        db.close()
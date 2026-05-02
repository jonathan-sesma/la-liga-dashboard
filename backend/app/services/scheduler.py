from app.database import SessionLocal
from app.services.teams_service import sync_teams
from app.services.standings_service import sync_standings
import logging
import asyncio

logger = logging.getLogger(__name__)

def sync_la_liga_data():
    logger.info("Scheduled Sync Started: Updating La Liga Teams...")

    db = SessionLocal()
    try:
        asyncio.run(sync_teams(db=db, league_id=140))
        logger.info("Scheduled sync completed successfully.")

    except Exception as e:
        logger.error(f"Sync failed: {e}")

    finally:
        db.close()

def sync_la_liga_standings():
    logger.info("Scheduled Sync Started: Updating La Liga Standings...")

    db = SessionLocal()

    try:
        asyncio.run(sync_standings(db=db, league_id=140))
        logger.info("Scheduled sync completed successfully.")

    except Exception as e:
        logger.error(f"Sync failed: {e}")

    finally:
        db.close()
from app.database import SessionLocal
from app.services.teams_service import sync_teams
from app.services.standings_service import sync_standings
import logging
import asyncio
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

async def sync_teams_now(
        competition_id: int,
        season: int,
):
    logger.info("Scheduled Sync Started: Updating La Liga Teams...")

    db = SessionLocal()

    try:
        await sync_teams(
            db=db,
            competition_id=competition_id,
            season=season
        )
        
        logger.info("Scheduled sync completed successfully.")

    except Exception as e:
        logger.error(f"Sync failed: {e}")

    finally:
        db.close()

def sync_la_liga_standings():
    logger.info("Scheduled Sync Started: Updating La Liga Standings...")

    db = SessionLocal()

    try:
        asyncio.run(sync_standings(db=db, league_id=140, season=2024))
        logger.info("Scheduled sync completed successfully.")

    except Exception as e:
        logger.error(f"Sync failed: {e}")

    finally:
        db.close()
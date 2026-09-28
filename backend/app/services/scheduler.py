from app.database import SessionLocal
from app.services.teams_service import sync_teams
from app.services.standings_service import sync_standings
import logging
import asyncio
# from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

async def sync_teams_now(
        competition_id: int,
        season: int,
):
    logger.info(f"Scheduled Sync Started: Updating competition: {competition_id} Teams...")

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

async def sync_standings_now(
        competition_id: int,
        season: int,
):
    logger.info(f"Scheduled Sync Started: Updating Competition: {competition_id} standings...")

    db = SessionLocal()

    try:
        await sync_standings(
            db=db,
            competition_id=competition_id,
            season=season
            
        )
        logger.info("Scheduled sync completed successfully.")

    except Exception as e:
        logger.error(f"Sync failed: {e}")

    finally:
        db.close()
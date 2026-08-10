from app.database import SessionLocal
from app.services.teams_service import sync_teams
from app.services.standings_service import sync_standings
import logging
import asyncio
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

def sync_teams_now(
        db: Session,
        competition_id: int | None = None,
        season: int | None = None,
):
    logger.info("Scheduled Sync Started: Updating La Liga Teams...")

    try:
        asyncio.run(sync_teams(db, competition_id, season))
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
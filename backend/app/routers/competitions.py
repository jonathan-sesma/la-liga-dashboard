from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.teams_service import get_or_sync_teams

router = APIRouter(prefix="/competitions", tags=["Competitions"])

@router.get("/{competition_id}/seasons/{season}/teams")
async def get_competition_teams(
        competition_id: int,
        season: int,
        db: Session = Depends(get_db)
):
    return await get_or_sync_teams(
        db = db,
        competition_id=competition_id,
        season=season,
    )

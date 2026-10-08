from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.standings_service import get_or_sync_standings
from app.schemas.standing import StandingResponse
from app.services.scheduler import sync_standings_now

router = APIRouter(prefix="/standings", tags=["Standings"])

@router.get("/{competition_id}/season/{season}", response_model=list[StandingResponse])
async def fetch_standings(
    competition_id: int,
    season: int,
    db: Session = Depends(get_db)
):
    return await get_or_sync_standings(
        db=db,
        competition_id=competition_id,
        season=season
    )

@router.post("/sync")
def manual_sync(
    background_tasks: BackgroundTasks,
    competition_id: int,
    season: int,
):
    background_tasks.add_task(
        sync_standings_now,
        competition_id=competition_id,
        season=season
    )
    return {"message": "Standings sync has been scheduled in the background"}
    
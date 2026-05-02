from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.standings_service import get_and_sync_standings
from app.schemas.standing import StandingResponse
from app.services.scheduler import sync_la_liga_standings

router = APIRouter(prefix="/standings", tags=["Standings"])

@router.get("/", response_model=list[StandingResponse])
async def fetch_standings(db: Session = Depends(get_db)):
    return await get_and_sync_standings(db=db, league_id=140)

@router.post("/sync_now")
def manual_sync(background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_la_liga_standings)
    return {"message": "Standings sync has been scheduled in the background"}
    
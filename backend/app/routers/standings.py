from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.standings_service import get_and_sync_standings, sync_standings

router = APIRouter(prefix="/standings", tags=["Standings"])

@router.get("/")
async def fetch_standings(db: Session = Depends(get_db)):
    return await get_and_sync_standings(db=db, league_id=140)

@router.post("/sync_now")
def manual_sync(background_task: BackgroundTasks):
    background_task.add_task(sync_standings)
    return {"message": "Standings sync has been scheduled in the background"}
    
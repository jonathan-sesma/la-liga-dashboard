from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.standings_service import get_and_sync_standings

router = APIRouter(prefix="/standings", tags=["Standings"])

@router.get("/")
async def fetch_standings(db: Session = Depends(get_db)):
    return await get_and_sync_standings(db=db, league_id=140)
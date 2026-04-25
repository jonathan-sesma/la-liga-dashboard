from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamResponse
from app.services.teams_service import get_and_sync_teams
from app.services.scheduler import sync_la_liga_data

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/", response_model=TeamResponse)
def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
    # team_data.model_dump() converts the Pydantic object to a dictionary
    new_team = Team(**team_data.model_dump())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@router.get("/")
async def fetch_teams(db: Session = Depends(get_db)):
    return await get_and_sync_teams(db=db, league_id=140) 

@router.post("/sync_now")
def manual_sync(background_tasks: BackgroundTasks):
    background_tasks.add_task(sync_la_liga_data)
    return {"message": "Team sync has been scheduled in the background."}
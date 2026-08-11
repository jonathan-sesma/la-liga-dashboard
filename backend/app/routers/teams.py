from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.teams_service import get_teams
from app.services.scheduler import sync_teams_now
# from app.models.team import Team
# from app.schemas.team import TeamCreate, TeamResponse

router = APIRouter(prefix="/teams", tags=["Teams"])

# @router.post("/", response_model=TeamResponse)
# def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
#     # team_data.model_dump() converts the Pydantic object to a dictionary
#     new_team = Team(**team_data.model_dump())
#     db.add(new_team)
#     db.commit()
#     db.refresh(new_team)
#     return new_team

@router.get("/")
async def fetch_teams(
    competition_id: int | None = None,
    season: int | None = None,
    db: Session = Depends(get_db),
):
    if season is not None and competition_id is None:
        raise HTTPException(
            status_code=400,
            detail="season requires competition_id"
        )
    
    return await get_teams(
        db = db,
        competition_id=competition_id,
        season=season,
    )

@router.post("/sync_now")
def manual_sync(
    background_tasks: BackgroundTasks,
    competition_id: int | None = None,
    season: int | None = None,
    db: Session = Depends(get_db),
):
    background_tasks.add_task(
        sync_teams_now,
        db=db,
        competition_id=competition_id,
        season=season
    )
    return {"message": "Team sync has been scheduled in the background."}
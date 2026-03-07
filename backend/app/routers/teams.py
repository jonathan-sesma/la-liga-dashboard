from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team import Team
from app.schemas.team import TeamCreate, TeamResponse

router = APIRouter(prefix="/teams", tags=["Teams"])

# We tell FastAPI to expect 'TeamCreate' in the body
# and return 'TeamResponse' as the result
@router.post("/", response_model=TeamResponse)
def create_team(team_data: TeamCreate, db: Session = Depends(get_db)):
    # team_data.model_dump() converts the Pydantic object to a dictionary
    new_team = Team(**team_data.model_dump())
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.team import Team

router = APIRouter(prefix="/teams", tags=["Teams"])

@router.post("/")
def create_team(name: str, city: str, stadium: str, db: Session = Depends(get_db)):
    team = Team(name=name, city=city, stadium=stadium)
    db.add(team)
    db.commit()
    db.refresh(team)
    return team

@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()
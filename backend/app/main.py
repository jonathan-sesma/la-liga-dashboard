from fastapi import FastAPI, Depends
from .database import engine, Base, get_db
from app.models.team import Team
from sqlalchemy.orm import Session

app = FastAPI(
    title="La Liga Statistics API",
    description="Backend API for La Liga Statistics dashboard",
    version="0.1.0"
)

@app.get("/")
def root():
    return {"status": "ok", "message": "La Liga API is running"}

Base.metadata.create_all(bind=engine)

@app.get("/teams")
def get_teams(db: Session = Depends(get_db)):
    return db.query(Team).all()
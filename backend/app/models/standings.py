from sqlalchemy import Column, Integer, ForeignKey
from app.database import Base

class Standings(Base):
    __tablename__ = "Standings"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"))
    league_id = Column(Integer, ForeignKey("teams.league_id"))
    position = Column(Integer)
    points = Column(Integer)
    played = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_difference = Column(Integer)
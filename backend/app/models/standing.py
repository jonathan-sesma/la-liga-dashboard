from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Standing(Base):
    __tablename__ = "standings"

    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    league_id = Column(Integer, ForeignKey("leagues.id"), index=True)

    position = Column(Integer)
    points = Column(Integer)
    played = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_difference = Column(Integer)

    league = relationship("League", back_populates="standings")
    team = relationship("Team", back_populates="standings")
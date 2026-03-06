from sqlalchemy import Column, String, Integer
from app.database import Base

class Standings(Base):
    __tablename__ = "Standings"

    team_id = Column(Integer, primary_key=True, index=True)
    points = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    draws = Column(Integer)
    position = Column(Integer)
    
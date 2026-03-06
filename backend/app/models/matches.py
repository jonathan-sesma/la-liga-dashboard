from sqlalchemy import Column, String, Integer
from app.database import Base

class Matches(Base):
    __tablename__= "Matches"

    id = Column(Integer, primary_key=True, index=True)
    home_team = Column(String)
    away_team = Column(String)
    home_score = Column(Integer)
    away_score = Column(Integer)
    date = Column(String)
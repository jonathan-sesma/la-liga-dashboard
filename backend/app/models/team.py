from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    stadium = Column(String)
    league_id = Column(Integer, index=True)

    standings = relationship("Standing", back_populates="team")
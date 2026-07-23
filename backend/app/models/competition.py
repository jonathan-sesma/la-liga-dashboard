from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Competition(Base):
    __tablename__ = "competitions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    country = Column(String)
    type = Column(String)

    team_seasons = relationship(
        "TeamCompetitionSeason",
        back_populates="competition"
    )

    standings = relationship(
        "Standing",
        back_populates="competition"
    )
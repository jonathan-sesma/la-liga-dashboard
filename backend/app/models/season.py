from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class Season(Base):
    __tablename__ = "seasons"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, unique=True, index=True)
    label = Column(String)

    team_competition_seasons = relationship(
        "TeamCompetitionSeason",
        back_populates="season"
    )

    standings = relationship(
        "Standing",
        back_populates="season"
    )
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    city = Column(String)
    stadium = Column(String)

    team_seasons = relationship(
        "TeamCompetitionSeason",
        back_populates="team"
    )

    standings = relationship(
        "Standing",
        back_populates="team"
    )
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class TeamCompetitionSeason(Base):
    __tablename__ = "team_competition_seasons"

    id = Column(Integer, primary_key=True, index=True)

    team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"), index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), index=True)

    team = relationship(
        "Team",
        back_populates="competition_seasons"
    )

    competition = relationship(
        "Competition",
        back_populates="team_seasons"
    )

    season = relationship(
        "Season",
        back_populates="team_competitions"
    )

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "competition_id",
            "season_id",
            name="uq_team_competition_season"
        ),
    )
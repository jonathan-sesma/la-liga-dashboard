from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.database import Base

class Standing(Base):
    __tablename__ = "standings"

    id = Column(Integer, primary_key=True, index=True)

    team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    competition_id = Column(Integer, ForeignKey("competitions.id"), index=True)
    season_id = Column(Integer, ForeignKey("seasons.id"), index=True)

    position = Column(Integer)
    points = Column(Integer)
    played = Column(Integer)
    wins = Column(Integer)
    draws = Column(Integer)
    losses = Column(Integer)
    goals_for = Column(Integer)
    goals_against = Column(Integer)
    goal_difference = Column(Integer)

    team = relationship(
        "Team",
        back_populates="standings"
    )

    competition = relationship(
        "Competition",
        back_populates="standings"
    )

    season = relationship(
        "Season",
        back_populates="standings"
    )

    __table_args__ = (
        UniqueConstraint(
            "team_id",
            "competition_id",
            "season_id",
            name="uq_team_competition_standing"
        ),
    )
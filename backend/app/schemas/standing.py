from pydantic import BaseModel, ConfigDict
from app.schemas.team import TeamBasic

class StandingBase(BaseModel):
    team_id: int
    league_id: int
    position: int
    points: int
    played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    goal_difference: int

class StandingResponse(StandingBase):
    team: TeamBasic
    
    model_config = ConfigDict(from_attributes=True)
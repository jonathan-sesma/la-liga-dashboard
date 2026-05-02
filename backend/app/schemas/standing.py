from pydantic import BaseModel, ConfigDict

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
    model_config = ConfigDict(from_attributes=True)
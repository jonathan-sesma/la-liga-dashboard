from pydantic import BaseModel, ConfigDict

class TeamBase(BaseModel):
    name: str
    city: str
    stadium: str
    league_id: int

class TeamCreate(TeamBase):
    pass 

class TeamResponse(TeamBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TeamBasic(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
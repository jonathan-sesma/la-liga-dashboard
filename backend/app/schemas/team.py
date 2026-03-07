from pydantic import BaseModel

class TeamBase(BaseModel):
    name: str
    city: str

class TeamCreate(TeamBase):
    pass 

class TeamResponse(TeamBase):
    id: int

    class Config:
        from_attibutes: True
from sqlalchemy import Column, Integer, String
from app.database import Base

class League(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True, index=True),
    name = Column(String, index=True),
    country = Column(String)
    season = Column(Integer)
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from app.database import get_db

# API_KEY = "e26353a17d32f2366cc2f5e5ab5ea0f8"

# BASE_URL = "https://v3.football.api-sports.io"

# headers = {
#     'x-apisports-key': API_KEY
# }

# router = APIRouter(tags=["football_api"], prefix="/football-api")

# @router.get("/")
# def get_standings(db: Session, Depends:(get_db)):

import httpx
from fastapi import HTTPException

API_KEY = "e26353a17d32f2366cc2f5e5ab5ea0f8"
BASE_URL = "https://v3.football.api-sports.io"

async def get_live_matches():
    headers = {
        'x-apisports-key': API_KEY
    }

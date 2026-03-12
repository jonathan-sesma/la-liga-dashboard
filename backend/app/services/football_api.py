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
from app.config import settings



async def get_live_matches():
    headers = {
        'x-apisports-key': settings.FOOTBALL_API_KEY
    }

    async with httpx.AsyncClient() as client:
        try:
            # We call the external endpoint to get live matches
            response = await client.get(f"{settings.FOOTBALL_API_URL}/fixtures?live=all", headers=headers)

            # This checks if api-football returned an error status code (like 400 or 500)
            response.raise_for_status()

            return response.json()
    
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=response.status_code, detail="Error fetching live matches from API-Football")
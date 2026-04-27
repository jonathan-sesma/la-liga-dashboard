import httpx
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config import settings

logger = logging.getLogger(__name__)
async def get_and_sync_standings(db: Session, league_id: int):
    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/standings?league={league_id}&season=2024"

    async with httpx.AsyncClient as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()["response"]

            for item in data:
                pass
                

        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail="Error fetching standings from API-FOOTBALL")
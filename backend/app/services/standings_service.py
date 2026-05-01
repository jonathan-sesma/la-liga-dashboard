import httpx
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config import settings
from app.models.standing import Standing

logger = logging.getLogger(__name__)
async def get_and_sync_standings(db: Session, league_id: int):
    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/standings?league={league_id}&season=2024"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()["response"][0]["league"]["standings"][0]

            for item in data:
                team_id = item["team"]["id"]

                existing = db.query(Standing).filter(
                    Standing.team_id == team_id,
                    Standing.league_id == league_id
                ).first()

                if existing:
                    existing.position = item["rank"]
                    existing.points = item["points"]
                    existing.played = item["all"]["played"]
                    existing.wins = item["all"]["win"]
                    existing.losses = item["all"]["lose"]
                    existing.draws = item["all"]["draw"]
                    existing.goals_for = item["all"]["goals"]["for"]
                    existing.goals_against = item["all"]["goals"]["against"]
                    existing.goal_difference = item["goalsDiff"]
                    
                else:
                    new_standing  = Standing(
                    team_id=team_id,
                    league_id=league_id,
                    position=item["rank"],
                    points=item["points"],
                    played=item["all"]["played"],
                    wins=item["all"]["win"],
                    losses=item["all"]["lose"],
                    draws=item["all"]["draw"],
                    goals_for=item["all"]["goals"]["for"],
                    goals_against=item["all"]["goals"]["against"],
                    goal_difference=item["goalsDiff"]
                    )

                    db.add(new_standing)

            db.commit()
            return db.query(Standing).filter(Standing.league_id == league_id).all()

        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code,detail="Error fetching standings from API-FOOTBALL")

async def sync_standings(db: Session, league_id: int):
    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/standings?league={league_id}&season=2024"

    async with httpx.AsyncClient as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
        
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error fetching standings from API-FOOTBALL")
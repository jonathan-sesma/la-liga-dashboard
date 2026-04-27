import json
import httpx
import logging
from fastapi import HTTPException
from app.config import settings
from sqlalchemy.orm import Session
from app.models import Team

logger = logging.getLogger(__name__)
async def get_and_sync_teams(db: Session, league_id: int):
    existing_teams = db.query(Team).filter(Team.league_id == league_id).all()

    if existing_teams:
        logger.info("Returning teams from Local Database")
        return existing_teams

    logger.info("Fetching from API-Football...")
    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/teams?league={league_id}&season=2024"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()

            data = response.json()["response"]

            for item in data:
                team_info = item["team"]
                venue = item["venue"]

                new_team = Team(
                    id=team_info["id"],
                    league_id=league_id,
                    name=team_info["name"],
                    city=venue["city"],
                    stadium=venue["name"]
                )

                db.add(new_team)
                
            db.commit()
            return db.query(Team).filter(Team.league_id == league_id).all()
    
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error fetching live matches from API-Football")
        



async def sync_teams(db: Session, league_id: int):
    logger.info("Syncing teams...")

    async with httpx.AsyncClient() as client:
        headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
        url = f"{settings.FOOTBALL_API_URL}/teams?league={league_id}&season=2024"

        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()["response"]

            logger.debug(f"API Response: {json.dumps(data[0], indent=2)}") # Debugging line to inspect the structure of the API response

            for item in data:
                team_info = item["team"]
                venue = item["venue"]

                existing_team = db.query(Team).filter(Team.id == team_info["id"]).first()

                if existing_team:
                    existing_team.name = team_info["name"]
                    existing_team.city = venue["city"]
                    existing_team.stadium = venue["name"]
                else:
                    new_team = Team(
                        id=team_info["id"],
                        league_id=league_id,
                        name=team_info["name"],
                        city=venue["city"],
                        stadium=venue["name"]
                    )
                    db.add(new_team)

            db.commit()
            logger.info(f"Sync complete! Updated {len(data)} teams.")
        
        except httpx.HTTPStatusError as exc:
            logger.error(f"Error syncing teams from API-Football: {exc}")
        except Exception as e:
            logger.error(f"Unexpected error during team sync: {e}")
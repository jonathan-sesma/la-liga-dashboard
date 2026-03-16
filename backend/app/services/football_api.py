import httpx
from fastapi import HTTPException
from app.config import settings
from sqlalchemy.orm import Session
from app.models import Team

async def get_and_sync_teams(db: Session, league_id: int):
    existing_teams = db.query(Team).filter(Team.league_id == league_id).all()

    if existing_teams:
        print("Returning teams from Local Database")
        return existing_teams

    print("Fetching from API-Football...")
    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/teams?league={league_id}&season=2023"

    async with httpx.AsyncClient() as client:
        try:
            # We call the external endpoint to get live matches
            response = await client.get(url, headers=headers)

            # This checks if api-football returned an error status code (like 400 or 500)
            response.raise_for_status()

            data = response.json()["response"]

            for item in data:
                team_info = item["team"]

                new_team = Team(
                    id=team_info["id"],
                    league_id=league_id,
                    name=team_info["name"],
                    city=team_info["city"],
                    stadium=item["venue"]["name"]
                )

                db.add(new_team)
                
            db.commit()
            return db.query(Team).filter(Team.league_id == league_id).all()
    
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail="Error fetching live matches from API-Football")
import httpx
import logging
from fastapi import HTTPException
from app.config import settings
from sqlalchemy.orm import Session
from app.models import Team

logger = logging.getLogger(__name__)

async def get_teams(
        db: Session,
        competition_id: int | None = None,
        season: int | None = None,
):
    teams = get_teams(
        db=db,
        competition_id=competition_id,
        season=season,
    )

    if teams:
        # logger.info("Returning teams from Local Database")
        return teams


    teams = await fetch_teams_from_api(
        competition_id=competition_id,
        season=season,
    )

    save_teams(
        db=db,
        teams=teams,
        competition_id=competition_id,
        season=season
    )

    return teams


async def sync_teams(
        db: Session,
        competition_id: int | None = None,
        season: int | None = None,
):
    teams = await fetch_teams_from_api(competition_id, season)

    save_teams(db, teams, competition_id)

    return get_teams(db, competition_id)


async def fetch_teams_from_api(competition_id, season) -> list:

    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/teams?league={competition_id}&season={season}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()["response"]
            return data
        except httpx.HTTPStatusError as exc:
            logger.exception("API-Football returned an error")
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Error fetching teams fron API-Football"
            )
        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(exc)}"
            )

def save_teams(db: Session, data, competition_id):
    existing_teams = db.query(Team).filter(
        Team.competition_id == competition_id
    ).all()

    existing_map = {
        team.id: team
        for team in existing_teams
    }

    try:
        for item in data:
            existing_team = existing_map.get(item["team"]["id"])

            if existing_team:
                existing_team.name = item["team"]["name"]
                existing_team.city = item["venue"]["city"]
                existing_team.stadium = item["venue"]["name"]
            else:
                new_team = Team(
                    id = item["team"]["id"],
                    name = item["team"]["name"],
                    city = item["venue"]["city"],
                    stadium = item["venue"]["name"]
                )

                db.add(new_team)
        db.commit()
    except Exception:
        db.rollback()
        raise

def get_teams(
        competition_id: int,
        season: int,
):
    
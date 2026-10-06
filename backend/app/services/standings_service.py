import httpx
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config import settings
from app.models.standing import Standing
from app.models.season import Season
from app.services.teams_service import get_or_create_season, get_teams_db

logger = logging.getLogger(__name__)

async def get_or_sync_standings(db: Session, competition_id: int, season: int):

    existing = get_standings_db(db, competition_id, season)

    if existing:
         return existing

    data = await fetch_standings_from_api(competition_id, season)

    upsert_standings(db, data, competition_id, season)

    return get_standings_db(db, competition_id, season)

async def sync_standings(db: Session, competition_id: int, season: int):

    data = await fetch_standings_from_api(competition_id, season)

    upsert_standings(db, data, competition_id, season)

    return get_standings_db(db, competition_id, season)

        
async def fetch_standings_from_api(competition_id, season) -> list:

    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/standings?league={competition_id}&season={season}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()["response"][0]["league"]["standings"][0]

            if response.json().get("errors"):
                logger.error(
                    "Api-Football error: %s",
                    response.json()["errors"]
                )

                raise HTTPException(
                    status_code=500,
                    detail=response.json()["errors"]
                )
            
            return data
        
        
        except httpx.HTTPStatusError as exc:
            logger.exception("API-FOOTBALL returned an error")
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Error fetching standings from API-FOOTBALL"
            )

        except Exception as exc:
            logger.exception("Unexpected error fetching standings")
            raise HTTPException(
                status_code=500,
                detail="Unexpected error fetching standings"
            )


def upsert_standings(db: Session, data, competition_id, season):

    season_obj = get_or_create_season(db, season)

    existing_teams = get_teams_db(db, competition_id, season)

    existing_standings = db.query(Standing).filter(
        Standing.competition_id == competition_id,
        Standing.season_id == season_obj.id
    ).all()
    
    existing_map = {
        standing.team_id: standing
        for standing in existing_standings
    }

    try:

        for item in data:
            existing_standing = existing_map.get(item["team"]["id"])

            if existing_standing:
                existing_standing.position = item["rank"]
                existing_standing.points = item["points"]
                existing_standing.played = item["all"]["played"]
                existing_standing.wins = item["all"]["win"]
                existing_standing.losses = item["all"]["lose"]
                existing_standing.draws = item["all"]["draw"]
                existing_standing.goals_for = item["all"]["goals"]["for"]
                existing_standing.goals_against = item["all"]["goals"]["against"]
                existing_standing.goal_difference = item["goalsDiff"]

            else:
                new_standing = Standing(
                team_id=item["team"]["id"],
                competition_id=competition_id,
                season_id=season,
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
    except Exception:
        db.rollback()
        raise


def get_standings_db(db: Session, competition_id, season) -> list[Standing]:

    season_obj = get_or_create_season(db, season)

    return db.query(Standing).filter(
        Standing.competition_id == competition_id,
        Standing.season_id == season_obj.id,
    ).all()
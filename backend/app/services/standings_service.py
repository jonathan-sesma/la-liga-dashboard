import httpx
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config import settings
from app.models.standing import Standing

logger = logging.getLogger(__name__)

async def get_and_sync_standings(db: Session, league_id: int):

    existing = get_standings(db, league_id)

    if existing:
         return existing

    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/standings?league={league_id}&season=2024"

    data = await fetch_standings_from_api(url, headers, db)

    upsert_standings(db, data, league_id)

    return get_standings(db, league_id)

async def sync_standings(db: Session, league_id: int):
    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/standings?league={league_id}&season=2024"

    data = await fetch_standings_from_api(url, headers, db)

    upsert_standings(db, data, league_id)

    return get_standings(db, league_id)

        
async def fetch_standings_from_api(url, headers, db):

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()["response"][0]["league"]["standings"][0]
            return data
        
        except httpx.HTTPStatusError as exc:
            db.rollback()
            raise HTTPException(
                status_code=exc.response.status_code,
                detail="Error fetching standings from API-FOOTBALL"
            )

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Unexpected error: {str(exc)}"
            )


def upsert_standings(db: Session, data, league_id):

    existing_standings = db.query(Standing).filter(
        Standing.league_id == league_id
    ).all()
    
    existing_map = {
        standing.team_id: standing
        for standing in existing_standings
    }

    try:

        for item in data:
            existing = existing_map.get(item["team"]["id"])

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
                new_standing = Standing(
                team_id=item["team"]["id"],
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
    except Exception:
        db.rollback()
        raise


def get_standings(db: Session, league_id):
    existing_stands = db.query(Standing).filter(
        Standing.league_id == league_id).all()
    
    if existing_stands:
        return existing_stands
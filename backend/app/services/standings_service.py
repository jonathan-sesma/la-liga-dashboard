import httpx
import logging
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.config import settings
from app.models.standing import Standing
from app.services.teams_service import get_or_create_season, get_teams_db, sync_teams

logger = logging.getLogger(__name__)

async def get_or_sync_standings(db: Session, competition_id: int, season_year: int):

    existing = get_standings_db(db, competition_id, season_year)

    if existing:
         return existing

    data = await fetch_standings_from_api(competition_id, season_year)

    await check_teams_exist_for_competition(db, data, competition_id, season_year)

    upsert_standings(db, data, competition_id, season_year)

    return get_standings_db(db, competition_id, season_year)

async def sync_standings(db: Session, competition_id: int, season_year: int):

    data = await fetch_standings_from_api(competition_id, season_year)

    upsert_standings(db, data, competition_id, season_year)

    return get_standings_db(db, competition_id, season_year)

        
async def fetch_standings_from_api(competition_id, season_year) -> list:

    headers = {'x-apisports-key': settings.FOOTBALL_API_KEY}
    url = f"{settings.FOOTBALL_API_URL}/standings?league={competition_id}&season={season_year}"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            payload = response.json()

        except httpx.HTTPStatusError as exc:
            logger.exception("API-Football returned an HTTP error")
            raise HTTPException(
                status_code=502,
                detail="Error fetching standing from API-FOOTBALL"
            ) from exc

        except (httpx.RequestError, ValueError) as exc:
            logger.exception("Failed to fetch or parse standings")
            raise HTTPException(
                status_code=502,
                detail="Unable to retrieve standings from API-FOOTBALL"
            ) from exc

    if payload.get("errors"):
        logger.error("API-FOOTBALL error: %s", payload["errors"])
        raise HTTPException(
            status_code=502,
            detail="API-FOOTBALL reported an error"
        )

    responses = payload.get("response", [])

    if not responses:
        raise HTTPException(
            status_code=404,
            detail="No standings found for this competition and season"
        )

    standings = responses[0]["league"]["standings"]

    if not standings:
        raise HTTPException(
            status_code=404,
            detail="No stanidngs table available"
        )

    return standings[0]

def upsert_standings(
    db: Session,
    data, 
    competition_id,
    season_year
):

    season_obj = get_or_create_season(db, season_year)

    existing_teams = get_teams_db(db, competition_id, season_year)

    existing_team_ids = {team.id for team in existing_teams}

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
            team_id = item["team"]["id"]

            if team_id not in existing_team_ids:
                raise ValueError(
                    f"Team {team_id} is missing from the database"
                )

            standing = existing_map.get(team_id)

            if standing is None:
                standing = Standing(
                    team_id=team_id,
                    competition_id=competition_id,
                    season_id=season_obj.id,
                )
                db.add(standing)
                existing_map[team_id] = standing

            standing.position = item["rank"]
            standing.points = item["points"]
            standing.played = item["all"]["played"]
            standing.wins = item["all"]["win"]
            standing.losses = item["all"]["lose"]
            standing.draws = item["all"]["draw"]
            standing.goals_for = item["all"]["goals"]["for"]
            standing.goals_against = item["all"]["goals"]["against"]
            standing.goal_difference = item["goalsDiff"]

        db.commit()

    except Exception:
        db.rollback()
        raise

def get_standings_db(db: Session, competition_id, season_year) -> list[Standing]:

    season_obj = get_or_create_season(db, season_year)

    return db.query(Standing).filter(
        Standing.competition_id == competition_id,
        Standing.season_id == season_obj.id,
    ).all()

async def check_teams_exist_for_competition(db, data, competition_id, season_year):

    teams = get_teams_db(db, competition_id, season_year)

    existing_team_ids = {team.id for team in teams}
    required_team_ids = {item["team"]["id"] for item in data}

    missing_team_ids = required_team_ids - existing_team_ids

    # for item in data:

    #     existing_team_competition = teams_map.get(item["team"]["id"])

    #     if existing_team_competition:
    #         pass

    #     else:
    #         await sync_teams(competition_id, season_year)

    #         teams = get_teams_db(db, competition_id, season_year)
            
    #         teams_map = {
    #             team.id: team
    #             for team in teams
    #         }
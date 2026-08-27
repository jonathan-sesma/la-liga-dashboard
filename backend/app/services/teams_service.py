import httpx
import logging
from fastapi import HTTPException
from app.config import settings
from sqlalchemy.orm import Session
from app.models import Team, Season
from app.models.team_competition_season import TeamCompetitionSeason

logger = logging.getLogger(__name__)

async def get_or_sync_teams(
        db: Session,
        competition_id: int,
        season: int,
):
    teams = get_teams_db(
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
        data=teams,
        competition_id=competition_id,
        season=season
    )

    return get_teams_db(
            db=db,
            competition_id=competition_id,
            season=season
        )


async def sync_teams(
        db: Session,
        competition_id: int,
        season: int,
):
    teams = await fetch_teams_from_api(
        competition_id,
        season,
    )

    save_teams(
        db=db,
        data=teams,
        competition_id=competition_id,
        season=season,
    )

    return get_teams_db(
        db=db,
        competition_id=competition_id,
        season=season
    )


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

def save_teams(
        db: Session,
        data: list,
        competition_id: int,
        season: int,
):
    season_obj = get_season_by_year(db, season)
    season_id = season_obj.id

    team_ids = [
        item["team"]["id"]
        for item in data
    ]

    existing_teams = (
        db.query(Team)
        .filter(Team.id.in_(team_ids))
        .all()
    )

    existing_team_map = {
        team.id: team
        for team in existing_teams
    }

    existing_relationships = (
        db.query(TeamCompetitionSeason)
        .filter(
            TeamCompetitionSeason.team_id.in_(team_ids),
            TeamCompetitionSeason.competition_id == competition_id,
            TeamCompetitionSeason.season_id == season_id,
        )
        .all()
    )

    existing_relationship_map = {
        (
            relationship.team_id,
            relationship.competition_id,
            relationship.season_id,
        ): relationship
        for relationship in existing_relationships
    }

    try:
        for item in data:
            team_data = item["team"]
            venue_data = item.get("venue") or {}

            team_id = team_data["id"]

            #update or create Team
            existing_team = existing_team_map.get(team_id)

            if existing_team:
                existing_team.name = team_data["name"]
                existing_team.city = venue_data.get("city")
                existing_team.stadium = venue_data.get("name")

            else:
                new_team = Team(
                    id=team_id,
                    name=team_data["name"],
                    city=venue_data.get("city"),
                    stadium=venue_data.get("name"),
                )

                db.add(new_team)

            # Create the Team ↔ Competition ↔ Season relationship
            relationship_key = (
                team_id,
                competition_id,
                season_id
            )

            if relationship_key not in existing_relationship_map:
                db.add(
                    TeamCompetitionSeason(
                        team_id=team_id,
                        competition_id=competition_id,
                        season_id=season_id
                    )
                )

        db.commit()

    except Exception:
        db.rollback()
        raise

def get_all_teams(db: Session):
    return db.query(Team).all()

def get_team_by_id(
        db: Session,
        team_id: int
):
    return (
        db.query(Team)
        .filter(Team.id == team_id)
        .first()
    )
    
def get_teams_db(
        db: Session,
        competition_id: int,
        season: int,
):
    season_obj = get_season_by_year(db, season)

    return ( db.query(Team)
            .join(
                TeamCompetitionSeason,
                TeamCompetitionSeason.team_id == Team.id,
        )
        .filter(
            TeamCompetitionSeason.competition_id == competition_id,
            TeamCompetitionSeason.season_id == season_obj.id
        )
        .all()
    )

def get_season_by_year(db: Session, year: int) -> Season:
    season_obj = (
        db.query(Season)
        .filter(Season.year == year)
        .first()
    )

    if season_obj is None:
        raise ValueError(f"Season {year} not found")

    return season_obj
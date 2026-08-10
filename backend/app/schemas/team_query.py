from pydantic import BaseModel, model_validator

class TeamQuery(BaseModel):
    competition_id: int | None = None
    season: int | None = None

    @model_validator(mode="after")
    def validate_season(self):
        if self.season is not None and self.competition_id is None:
            raise ValueError(
                "season requires competition_id"
            )

        return self
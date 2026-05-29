from typing import Any, Optional, TypeAlias, Literal
from datetime import datetime
from pydantic import BaseModel, model_validator, Field, field_validator

BookMakerName: TypeAlias = str


class MoneylineOdds(BaseModel):
    home: float
    away: float

class SpreadOdds(BaseModel):
    hdp: float
    home: float
    away: float

class TotalsOdds(BaseModel):
    hdp: float
    over: float
    under: float

class OddsEntry(BaseModel):
    name: Literal["ML", "Spread", "Totals"]
    updated_at: datetime = Field(alias="updatedAt") 
    odds: list[MoneylineOdds | SpreadOdds | TotalsOdds]

    @property
    def current_odds(self) -> MoneylineOdds | SpreadOdds | TotalsOdds:
        return self.odds[0]

class Bookmaker(BaseModel):
    name: str
    id: int


class Sport(BaseModel):
    name: str
    slug: str


class League(BaseModel):
    name: str
    slug: str
    sport: Sport


class Team(BaseModel):
    id: int
    name: str
    slug: str
    sport: Sport


class Event(BaseModel):
    id: str
    sport: Sport
    home_team: Team
    away_team: Team
    date: str
    league: League
    status: Optional[str] = None
    odds_history: Optional[list[OddsEntry]] = None

    @model_validator(mode="before")
    @classmethod
    def transform_event_data(cls, data: dict[str, Any]) -> dict[str, Any]:
        # Convert id to string if it's an int
        if isinstance(data["id"], int):
            data["id"] = str(data["id"])

        # Create home_team from home and homeId
        data["home_team"] = {
            "id": data["homeId"],
            "name": data["home"],
            "slug": data["home"].lower().replace(" ", "-"),
            "sport": data["sport"],
        }

        # Create away_team from away and awayId
        data["away_team"] = {
            "id": data["awayId"],
            "name": data["away"],
            "slug": data["away"].lower().replace(" ", "-"),
            "sport": data["sport"],
        }

        # Add sport to league
        data["league"]["sport"] = data["sport"]

        return data

class EventOdds(BaseModel):
    id: str
    home: str
    away: str
    date: datetime
    status: str

    bookmakers: dict[str, list[OddsEntry]]

    @field_validator("id", mode="before")
    @classmethod
    def id_to_string(cls, v: int | str) -> str:
        return str(v)

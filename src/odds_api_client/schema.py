from typing import Optional, TypeAlias

from pydantic import BaseModel, model_validator

BookMakerName: TypeAlias = str


class Odds(BaseModel):
    home_win: float
    away_win: float


class OddsEntry(BaseModel):
    name: str
    odds: Odds
    update_time: str


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
    def transform_event_data(cls, data):
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

    @property
    def get_opening_odds(self) -> Optional[Odds]:
        if self.odds_history and len(self.odds_history) > 0:
            return self.odds_history[0].odds
        return None

    @property
    def get_latest_odds(self) -> Optional[Odds]:
        if self.odds_history and len(self.odds_history) > 0:
            return self.odds_history[-1].odds
        return None

    @property
    def get_closing_odds(self) -> Optional[Odds]:
        if self.odds_history and len(self.odds_history) > 0:
            return self.odds_history[-1].odds if self.status != "pending" else None
        return None

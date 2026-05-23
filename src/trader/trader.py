import logging
import os
from logging.handlers import RotatingFileHandler

from schema import Bookmaker, Event, League, OddsEntry, Sport

from odds_api_client import OddsApiClient


class OddsTracker:
    def __init__(
        self,
        sport: Sport,
        leagues: list[League],
        bookmakers: list[Bookmaker],
        odds_api_client: OddsApiClient,
    ):

        self.odds_api_client = odds_api_client
        self.sport = sport
        self.leagues = leagues
        self.bookmakers = bookmakers
        self.odds_data: dict[str, list[OddsEntry]] = {}
        self.upcoming_events: dict[str, list[Event]] = {}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        os.makedirs("logs", exist_ok=True)

        # File handler
        file_handler = RotatingFileHandler(
            "logs/odds_tracker.log", maxBytes=5_000_000, backupCount=3
        )
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

        self.logger.info("OddsTracker initialized")

    def get_events(self, league_slug: str, status: str) -> list[Event]:
        events = self.odds_api_client.get_events(
            sport=self.sport.slug, league=league_slug, status=status
        )
        return [Event(**event) for event in events]

    def get_event_odds(self, event_id: str, bookmaker: Bookmaker) -> list[OddsEntry]:
        odds = self.odds_api_client.get_event_odds(
            event_id=event_id, bookmakers=[bookmaker.name]
        )
        return [OddsEntry(**odd) for odd in odds]

    def add_new_events(self, events: list[Event]) -> None:
        for event in events:
            self.logger.info(f"Proccessing event: {event}")
            league_name = event.league.name
            if league_name not in self.upcoming_events:
                self.upcoming_events[league_name] = []
            if event not in self.upcoming_events[league_name]:
                self.upcoming_events[league_name].append(event)
                self.logger.info(f"Added new event: {event}")

        self.logger.info(f"Upcoming events: {self.upcoming_events}")

    def update_odds_history(self, event_id: str, odds_entry: OddsEntry) -> None:
        if event_id not in self.odds_data:
            self.odds_data[event_id] = []
        self.odds_data[event_id].append(odds_entry)
        self.logger.info(
            f"Updated odds history for event ID {event_id}: {self.odds_data[event_id]}"
        )

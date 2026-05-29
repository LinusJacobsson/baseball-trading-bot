import time
from enum import Enum

from trading_bot.api.odds_api_client import OddsApiClient
from trading_bot.api.schema import Event
from trading_bot.core.config import settings


class GameState(str, Enum):
    PENDING = "pending"
    LIVE = "live"
    SETTLED = "settled"

class Sport(str, Enum):
    BASEBALL = "baseball"

class Trader:
    def __init__(self, odds_api_client: OddsApiClient) -> None:
        self.odds_api_client = odds_api_client
        self.matches: dict[str, Event] = {}


    def get_matches(
        self,
        sport: Sport,
        game_state: GameState,
        league: str,
        bookmaker: str = "Bet365"
    ) -> None:
        incoming_events = self.odds_api_client.get_events(
            status=game_state.value,
            sport=sport.value,
            league=league,
            bookmaker=bookmaker,
        )
        print(f"Found events: {incoming_events}")
        for event in incoming_events:
            if event.id not in self.matches:
                print(f"Adding event: {event.id} to tracked matches")
                self.matches[event.id] = event
            else:
                print(f"Event {event.id} already exists in tracked events")


    def get_event_odds(self, event_id: str, bookmakers: list[str] = ["Bet365"]) -> None:
        event_odds = self.odds_api_client.get_event_odds(event_id=event_id, bookmakers=bookmakers)
        print(f"Fetched event odds: {event_odds}")

if __name__ == "__main__":
    client = OddsApiClient(api_key=settings.odds_api_key)
    trader = Trader(odds_api_client=client)
    while True:
        trader.get_matches(
        sport=Sport.BASEBALL,
        game_state=GameState.PENDING,
        league="chinese-taipei-cpbl"
        )
        first_item = list(trader.matches.items())[0]
        print(f"Första match-ID: {first_item[0]}, Objekt: {first_item[1]}")
        trader.get_event_odds(event_id=first_item[0])
        time.sleep(30)




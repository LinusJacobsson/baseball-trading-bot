import os
from enum import Enum
from typing import Any
from trading_bot.api.odds_api_client import OddsApiClient
import time

class GameState(str, Enum):
    PENDING = "pending"
    LIVE = "live"
    SETTLED = "settled"

class Sport(str, Enum):
    BASEBALL = "baseball"

class Trader:
    def __init__(self, odds_api_client: OddsApiClient) -> None:
        self.odds_api_client = odds_api_client
        self.matches = {}


    def get_matches(self, sport: Sport,  game_state: GameState) -> list[Any]:
        incoming_events = self.odds_api_client.get_events(status=game_state.value, sport=sport.value)
        for event in incoming_events:
            if event.id not in self.matches:
                print(f"Adding event: {event.id} to tracked matches")
                self.matches[event.id] = event
            else:
                print(f"Event {event.id} already exists in tracked events")




if __name__ == "__main__":
    API_KEY = os.getenv("ODDS_API_KEY")
    client = OddsApiClient(api_key=API_KEY)
    trader = Trader(odds_api_client=client)
    while True:
        trader.get_matches(sport=Sport.BASEBALL, game_state=GameState.PENDING)
        first_item = list(trader.matches.items())[0]
        print(f"Första match-ID: {first_item[0]}, Objekt: {first_item[1]}")
        time.sleep(30)




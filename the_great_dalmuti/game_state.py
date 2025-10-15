from typing import *

if TYPE_CHECKING:
    from player import Player


class GameState:
    def __init__(self, players) -> None:
        self.players: List[Player] = players
        self._current_round: List[Tuple[str, List[int]]] = []
    
    def __repr__(self) -> str:
        return f"""
{self._current_round}
{self.get_player_card_count}
"""

    def clear_current_round(self) -> None:
        self._current_round = []

    def get_current_round(self) -> List[Tuple[str, List[int]]]:
        return self._current_round

    def add_to_current_round(self, player_name: str, cards: List[int]) -> None:
        self._current_round.append((player_name, cards))

    def get_player_card_count(self) -> Dict[str, int]:
        return {player.name: player.num_cards for player in self.players}

    def get_last_played(self) -> List[int] | None:
        for _, cards in reversed(self._current_round):
            if cards:
                return cards

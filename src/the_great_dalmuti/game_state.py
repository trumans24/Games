from typing import *

if TYPE_CHECKING:
    from the_great_dalmuti.player import Player, CPU, Human


class GameState:
    def __init__(self, players: List["Player"]) -> None:
        self.players: List["Player"] = players
        self._current_round: List[Tuple[str, List[int]]] = []
    
    def __repr__(self) -> str:
        return f"""
{self._current_round}
{self.get_player_card_count()}
"""

    def valid_play(self, cards: List[int]) -> bool:
        last_played = self.get_last_played()
        if not (last_played and cards):
            return True
        
        last_played_card = ((set(last_played) - {13}) or {13}).pop()
        
        if len(cards) != len(last_played):
            print("You must play the same number of cards as the last played.")
            return False
        
        if any(card >= last_played_card for card in cards if card != 13):
            print("You must play cards lower than the last played (excluding wilds).")
            return False
        return True

    def clear_current_round(self) -> None:
        self._current_round = []

    def get_current_round(self) -> List[Tuple[str, List[int]]]:
        return self._current_round

    def add_to_current_round(self, player_name: str, cards: List[int]) -> None:
        if not self.valid_play(cards):
            print(f"Invalid play attempted by {player_name} with cards {cards} on {self.get_last_played()}")
        assert self.valid_play(cards)
        self._current_round.append((player_name, cards))

    def get_player_card_count(self) -> Dict[str, int]:
        return {player.name: player.num_cards for player in self.players}

    def get_last_played(self) -> List[int] | None:
        """
        Returns the last played cards in the current round. Ignores players that passed. If no cards have been played, returns None.
        """
        for _, cards in reversed(self._current_round):
            if cards:
                return cards

from typing import *
from game_state import GameState

class Player:
    def __init__(self, name) -> None:
        self.name: str = name
        self._cards: List[int] = []

    @property
    def num_cards(self):
        return len(self._cards)

    def has_cards(self) -> bool:
        return len(self._cards) > 0
    
    def get_valid_cards(self, cards: List[int]) -> List[int]:
        valid_cards = []
        for card in self._cards:
            if card < cards[0] and self._cards.count(card) >= len(cards):
                valid_cards.append(card)
        return valid_cards


    def add_cards(self, cards: int | List[int]) -> None:
        self._cards.extend(cards)
        self._cards.sort()

    def give_low_cards(self, num_of_cards) -> List[int]:
        pass

    def give_any_cards(self, num_of_cards) -> List[int]:
        pass

    def play(self, game_state) -> List[int]:
        pass

class CPU(Player):
    def give_low_cards(self, num_of_cards) -> List[int]:
        assert num_of_cards <= self._cards
        cards = []
        for _ in range(num_of_cards):
            cards.append(self._cards.pop(0))
        return cards

    def give_any_cards(self, num_of_cards) -> List[int]:
        assert num_of_cards <= self._cards
        cards = []
        for _ in range(num_of_cards):
            cards.append(self._cards.pop())
        return cards
    
    def play(self, game_state: GameState) -> List[int]:
        last_played = game_state.get_last_played()
        if not last_played:
            return []
        valid_cards = self.get_valid_cards(last_played)
        if not valid_cards:
            return []
        card = valid_cards.pop()
        card_count = self._cards.count(card)
        while card in self._cards:
            self._cards.remove(card)
        return [card] * card_count


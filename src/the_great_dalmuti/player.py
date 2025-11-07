import click
import random
from typing import List
from the_great_dalmuti.game_state import GameState
from the_great_dalmuti.input_util import prompt

class Player:
    def __init__(self, name) -> None:
        self.name: str = name
        self._cards: List[int] = []

    @property
    def num_cards(self) -> int:
        return len(self._cards)

    @property
    def num_wilds(self) -> int:
        return self._cards.count(13)

    def has_cards(self) -> bool:
        return len(self._cards) > 0
    
    def get_valid_cards(self, cards: List[int] | None) -> List[int]:
        if not cards:
            return self._cards.copy()
        valid_cards = []
        for card in self._cards:
            if card == 13:
                continue
            elif card < (set(cards) - {13} or {13}).pop() and self._cards.count(card) >= len(cards) - self.num_wilds:
                valid_cards.append(card)
            if 13 not in valid_cards and self._cards.count(card) + self.num_wilds >= len(cards):
                valid_cards.extend([13] * self.num_wilds)
        valid_cards.sort()
        return valid_cards

    def valid_play(self, game_state: GameState, cards: List[int]) -> bool:
        """
        Makes sure the play is valid.
        1. Passing is always valid.
        2. All cards played are the same (excluding wilds).
        3. Player has the cards they are trying to play.
        4. If there is a last played, the number of cards played is the same as the last played.
        5. If there is a last played, the cards played are lower than the last played (excluding wilds).
        """
        if not cards:
            return True
        
        if len(set(cards) - {13}) > 1:
            print("All cards played must be the same (excluding wilds).")
            return False
        
        if any(cards.count(card) > self._cards.count(card) for card in cards):
            print("You do not have the cards you are trying to play.")
            return False

        return game_state.valid_play(cards)


    def add_cards(self, cards: int | List[int]) -> None:
        self._cards.extend([cards] if isinstance(cards, int) else cards)
        self._cards.sort()

    def give_low_cards(self, num_of_cards) -> List[int]: # type: ignore
        pass

    def give_any_cards(self, num_of_cards) -> List[int]: # type: ignore
        pass

    def play(self, game_state) -> List[int]: # type: ignore
        pass

class Human(Player):
    def remove_cards(self, cards: List[int] | int) -> List[int]:
        if isinstance(cards, int):
            cards = [cards]
        for card in cards:
            if card in self._cards:
                self._cards.remove(card)
        return cards
    
    def give_low_cards(self, num_of_cards: int) -> List[int]:
        assert num_of_cards <= self.num_cards
        cards = []
        for _ in range(num_of_cards):
            cards.append(self._cards.pop(0))
        click.echo(f'Giving these low cards to your opponent: {cards}.')
        return cards
    
    def give_any_cards(self, num_of_cards: int) -> List[int]:
        cards = []
        for i in range(1, num_of_cards + 1):
            card = prompt(
                f'What card do you want to give your opponent (card {i} of {num_of_cards})? You have {self._cards}',
                type=click.Choice(self._cards + ['q', 'quit', 'exit']),
                show_choices=False,
            )
            cards.extend(self.remove_cards(card))
        return cards
    
    def play(self, game_state: GameState) -> List[int]:
        while True:
            card = prompt(
                f'What cards do you want to play? You have {self._cards}',
                type=click.Choice(self._cards + ['q', 'quit', 'exit', '']),
                show_choices=False,
                default='',
                show_default=False
            )
            if not card:
                return []
            len_to_play = len(game_state.get_last_played() or [])
            if len_to_play and len_to_play <= self._cards.count(card):
                cards = [card] * len_to_play
            elif len_to_play:
                cards = [card] * self._cards.count(card) + [13] * (len_to_play - self._cards.count(card))
            else:
                if self._cards.count(card) > 1:
                    if click.confirm(f'Do you want to play all your {card}s?', default=True):
                        cards = [card] * self._cards.count(card)
                    else:
                        count = prompt(f'How many {card}s do you want to play?', type=click.IntRange(min=1, max=self._cards.count(card)))
                        cards = [card] * count
                else:
                    cards = [card]
            
            if self.valid_play(game_state, cards):
                break
            click.echo('Invalid response. Please try again.')
        return self.remove_cards(cards)


class CPU(Player):
    def give_low_cards(self, num_of_cards) -> List[int]:
        assert num_of_cards <= self.num_cards
        cards = []
        for _ in range(num_of_cards):
            cards.append(self._cards.pop(0))
        return cards

    def give_any_cards(self, num_of_cards) -> List[int]:
        assert num_of_cards <= self.num_cards
        cards = []
        for _ in range(num_of_cards):
            cards.append(self._cards.pop())
        return cards
    
    def play_any(self) -> List[int]:
        i = -1
        card = self._cards[i]
        while card == 13 and abs(i) <= len(self._cards):
            card = self._cards[i]
            i -= 1
        card_count = self._cards.count(card)
        while card in self._cards:
            self._cards.remove(card)
        return [card] * card_count

    def choose_valid(self, valid_cards: List[int], last_played: List[int]) -> List[int]:
        last_played_card = (set(last_played) - {13} or {13}).pop()
        for card in reversed(valid_cards):
            if card >= last_played_card or self._cards.count(card) > len(last_played):
                continue
            elif self._cards.count(card) == len(last_played):
                card_count = self._cards.count(card)
                while card in self._cards:
                    self._cards.remove(card)
                return [card] * card_count
            elif self._cards.count(card) + self.num_wilds >= len(last_played):
                cards_to_play = [card] * self._cards.count(card) + [13] * (len(last_played) - self._cards.count(card))
                assert cards_to_play.count(13) <= self._cards.count(13)
                for card in cards_to_play:
                    self._cards.remove(card)
                return cards_to_play
        return []
    
    def play(self, game_state: GameState) -> List[int]:
        if not self.num_cards:
            return []
        last_played = game_state.get_last_played()
        if not last_played:
            return self.play_any()
        valid_cards = self.get_valid_cards(last_played)
        
        return self.choose_valid(valid_cards, last_played)



class CPU2(CPU):
    def play_any(self) -> List[int]:
        card_Set = set(self._cards) - {13} or {13}
        # pick a random card from the set
        card = random.choice(list(card_Set))
        card_count = self._cards.count(card)
        while card in self._cards:
            self._cards.remove(card)
        return [card] * card_count
    
    def choose_valid(self, valid_cards: List[int], last_played: List[int]) -> List[int]:
        # return a random valid play
        valid_set = set(valid_cards) - {13} or {13}
        card = random.choice(list(valid_set))
        if card == 13 and len(valid_set) > 1:
            print('what is going on?????????????????????????')
        if self._cards.count(card) >= len(last_played):
            card_count = len(last_played)
            for _ in range(card_count):
                self._cards.remove(card)
            return [card] * card_count
        elif self._cards.count(card) + self.num_wilds >= len(last_played):
            print(f"CPU2 choosing valid play with card {card}, last_played {last_played}, cards {self._cards}, valid_cards {valid_cards}, {self._cards.count(card)}, {self.num_wilds}, {len(last_played)}")
            cards_to_play = [card] * self._cards.count(card) + [13] * (len(last_played) - self._cards.count(card))
            assert cards_to_play.count(13) <= self._cards.count(13)
            for card in cards_to_play:
                self._cards.remove(card)
            return cards_to_play
        return []

if __name__ == "__main__":
    """
    Makes sure the play is valid.
    1. Passing is always valid.
    2. All cards played are the same (excluding wilds).
    3. Player has the cards they are trying to play.
    4. If there is a last played, the number of cards played is the same as the last played.
    5. If there is a last played, the cards played are lower than the last played (excluding wilds).
    """
    # test all the cases for valid_play
    player = CPU("Test")
    player.add_cards([1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 13, 13])
    game_state = GameState([player])
    
    assert player.valid_play(game_state, []) == True # passing
    assert (player.valid_play(game_state, [1, 2]) == False) and (player.valid_play(game_state, [1, 13]) == True) # different cards
    assert (player.valid_play(game_state, [6]) == False) and (player.valid_play(game_state, [1, 1]) == False) # cards not in hand
    game_state.add_to_current_round(player.name, [9, 9])
    game_state.add_to_current_round(player.name, [5, 5])
    game_state.add_to_current_round(player.name, [])
    assert (player.valid_play(game_state, [3, 3, 3]) == False) and (player.valid_play(game_state, [3]) == False) # wrong number of cards
    assert (player.valid_play(game_state, [6, 6]) == False) and (player.valid_play(game_state, [5, 5]) == False) and (player.valid_play(game_state, [4, 4]) == True) # not lower than last played
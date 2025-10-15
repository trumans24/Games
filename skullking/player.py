from game import Game
from cards import special, winning_special, Card
from random import choice, random
from typing import List, Dict, Self, Iterable
from util import print_game

class Player:
    def __init__(self, name: str, cards: list[Card] = None) -> None:
        """
        Initialize a new player.
        
        Args:
            name (str): Player's name
            cards (list[Card], optional): Initial hand of cards. Defaults to empty list.
        
        Attributes:
            name (str): Player's name
            cards (list[Card]): Player's current hand
            current_bet (int): Player's bet for current round
            tricks_won (int): Number of tricks won in current round
        """
        self.name: str = name
        self.cards: list[Card] = cards if cards is not None else []
        self.current_bet: int = 0
        self.tricks_won: int = 0

    def __repr__(self) -> str:
        """
        Return string representation of the player.
        
        Returns:
            str: Player name and their current cards
        """
        return f'{self.name}: {self.cards}'

    def add_card(self, card: Card) -> None:
        """
        Add a card to the player's hand.
        
        Args:
            card (Card): Card to add to the hand
        """
        if self.cards is not None:
            self.cards.append(card)
        else:
            self.cards = [card]

    def set_cards(self, cards: list[Card]) -> None:
        """
        Set the player's hand to a new set of cards.
        
        Args:
            cards (list[Card]): New hand of cards
        """
        self.cards = cards

    def play(self, current_trick: Dict[Self, Card], trump_color: str, number_of_players: int = 0) -> str: # type: ignore
        pass

    def bet(self, number_of_players: int) -> int: # type: ignore
        pass

    def valid_cards(self, cards: Iterable[Card]) -> List[Card]:
        valid_card_list = []
        trump_color = Game.get_trump_color(cards)
        have_trump = False
        for card in self.cards:
          if card in special or card.color in ['black', trump_color]:
            valid_card_list.append(card)
          if card.color == trump_color:
            have_trump = True
        if have_trump:
            return valid_card_list
        return self.cards

class Human(Player):
    def play(self, current_trick: Dict[Player, Card], trump_color:str, number_of_players:int = 0) -> str:
        # if len(self.cards) == 1:
        #     card = self.cards[0]
        #     self.cards.remove(card)
        #     return Card(card)
        # print('Cards that have already been played in this trick:', current_trick if len(current_trick) > 0 else None)
        print_game(title='Cards Played', stats=current_trick, message=f'What card would you like to play {self.cards}?')
        print('What card would you like to play? Cards in hand:', self.cards)
        while True:
            try:
                response = input(f'Please select the card you would like to play: (Trump color is {trump_color if trump_color else "any"}) ')
                if response in ['e', 'q', 'exit', 'esc']:
                    exit(1)
                card = Card(response)
                print('current trick:', current_trick.values())
                print('valid_Cards:', self.valid_cards(current_trick.values()))
                assert card in self.valid_cards(current_trick.values())
                self.cards.remove(card)
                if card == 'tigress':
                    while card not in ['pirate', 'pass']:
                        card = input('Would you like to play "pirate" or "pass"? ')
                try:
                    return Card(card)
                except:
                    print('Not a valid option.')
            except (ValueError, IndexError):
                print('Not a valid card.')
            except AssertionError:
                print('You must follow suit or play a special card.')


    def bet(self, number_of_players: int) -> int:
        """
        Human player bet selection with interactive input.
        
        Args:
            number_of_players (int): Number of players in the game
        
        Returns:
            int: Number of tricks the player bets to win
        
        Interactive flow:
        1. Display current hand
        2. Get player input for bet amount
        3. Validate bet is within allowed range
        """
        print('_'*100)
        print('Please make your bet. Cards in hand:', self.cards)
        while True:
            try:
                response = input(f'What would you like to bet? (Max bet is {len(self.cards)}) ')
                if response in ['e', 'q', 'exit', 'esc']:
                    exit(1)
                return int(response)
            except ValueError:
                print('Not a valid bet.')

class CPU(Player):
    def play(self, current_trick: Dict[Player, Card], trump_color:str, number_of_players:int = 0) -> str:
        if len(self.cards) == 1:
            return self.cards.pop()
        valid_card_list = self.valid_cards(current_trick.values())
        card = choice(valid_card_list)
        self.cards.remove(card)
        if card == 'tigress':
            card = Card('pirate' if random() >= 0.5 else 'pass')
        return card

    def try2win(self, current_trick: Dict[Player, Card], trump_color:str):
        winners = set(self.cards) & set(winning_special)
        cards_list = list(current_trick.values())
        for card in winners:
            if card == Game.winning_card(cards_list):
                continue
            elif card == Game.winning_card(cards_list+[card]):
                return card

        for card in [card for card in self.cards if card.color == 'black']:
            if card == Game.winning_card(cards_list):
                continue
            elif card == Game.winning_card(cards_list+[card]):
                return card

        if card := self.card_in_color(trump_color, best=False):
            return card

        for card in self.cards:
            if card == Game.winning_card(cards_list):
                continue
            elif card == Game.winning_card(cards_list+[card]):
                return card
        return self.cards[0]

    def try2lose(self, current_trick: Dict[Player, Card], trump_color:str):
        if len(current_trick) == 0:
            non_winning = set(self.cards) - set(winning_special)
            if len(non_winning) > 0:
                return sorted(non_winning, key=lambda x: x.number)[0]
            return self.cards[0]
        cards_list = list(current_trick.values())
        winning_card = Game.winning_card(cards_list)
        if 'white_whale' in cards_list and winning_card:
            if 'skullking' in self.cards:
                return Card('skullking')
            elif 'pirate' in self.cards:
                return Card('pirate')
            elif 'mermaid' in self.cards:
                return Card('mermaid')
            best_black = self.card_in_color('black', max_value=winning_card.number)
            if best_black and best_black.number <= winning_card.number:
                return best_black
            if best_trump := self.card_in_color(trump_color, max_value=winning_card.number):
                return best_trump
            best_yellow = self.card_in_color('yellow', max_value=winning_card.number)
            best_green = self.card_in_color('green', max_value=winning_card.number)
            best_purple = self.card_in_color('purple', max_value=winning_card.number)
            options = [card for card in (best_yellow, best_green, best_purple) if card]
            filtered = filter(lambda x: x.number <= winning_card.number if x else Card('black-14'), options)
            best = next(iter(sorted(filtered, key=lambda x: x.number)), None)
            if best is not None:
                return best
            # print('White whale was played and was not able to find card', current_trick, self.cards)
            return self.cards[0]
        if 'kraken' in cards_list and winning_card:
            if 'skullking' in self.cards:
                return Card('skullking')
            elif 'pirate' in self.cards:
                return Card('pirate')
            elif 'mermaid' in self.cards:
                return Card('mermaid')
            best_black = self.card_in_color('black')
            if best_black:
                return best_black
            if best_trump := self.card_in_color(trump_color):
                return best_trump
            best_yellow = self.card_in_color('yellow')
            best_green = self.card_in_color('green')
            best_purple = self.card_in_color('purple')
            options = [card for card in (best_yellow, best_green, best_purple) if card]
            best = next(iter(sorted(options, key=lambda x: x.number, reverse=True)), None)
            if best is not None:
                return best
            # print('Kraken was played and was not able to find card', current_trick, self.cards)
            return self.cards[0]

        if card := self.card_in_color(trump_color):
            return card

        for card in self.cards:
            if card == Game.winning_card(cards_list):
                return card
            elif card != Game.winning_card(cards_list+[card]):
                return card
        return card

    def card_in_color(self, color: str, best: bool = True, max_value: int = 14, min_value: int = 1) -> Card:
        """
        Find the best card of a specific color in hand.
        
        Args:
            color (str): Color to search for
            best (bool, optional): Whether to find best (highest) card. Defaults to True.
            max_value (int, optional): Maximum card value to consider. Defaults to 14.
            min_value (int, optional): Minimum card value to consider. Defaults to 1.
        
        Returns:
            Card: Best card of the specified color, or empty string if none found
        
        Logic:
        - If best=True: finds highest card under max_value
        - If best=False: finds lowest card above min_value
        """
        candidate = ''
        for card in sorted(self.cards, key=lambda x: x.number, reverse=not best):
            if card.color == color:
                if not candidate:
                    candidate = card
                elif (candidate.number < card.number < max_value) if best else (min_value < card.number < candidate.number):
                    candidate = card
        return candidate

    def bet(self, number_of_players:int):
        card_colors = [card.color for card in self.cards]
        bet = card_colors.count('skullking') + card_colors.count('pirate') + card_colors.count('mermaid') + card_colors.count('black') // 2
        self.current_bet = bet
        return bet  # random.randint(0, min(len(self.cards), 4))

# class Vision(CPU):
#     def look_at_card(self) -> None:
#         card = identify_card()
#         self.add_card(Card(card))


# class AI(CPU):
#   pass
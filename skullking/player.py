from game import Game
from cards import special, winning_special, Card
from random import choice, random
class Player:
    def __init__(self, name, cards=None) -> None:
        self.name = name
        self.cards = cards if cards is not None else []
        self.current_bet = 0
        self.tricks_won = 0

    def __repr__(self):
        return f'{self.name}: {self.cards}'

    def add_card(self, card: str) -> None:
        if self.cards is not None:
            self.cards.append(card)
        else:
            self.cards = [card]

    def set_cards(self, cards: list) -> None:
        self.cards = cards

    def play(self, current_trick:list, trump_color:str, number_of_players:int = 0) -> str:
        pass

    def bet(self, number_of_players:int):
        pass

    def valid_cards(self, cards):
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
    def play(self, current_trick: list, trump_color:str, number_of_players:int = 0) -> str:
        print('_'*100)
        print('Cards that have already been played in this trick:', current_trick if len(current_trick) > 0 else None)
        print('What card would you like to play? Cards in hand:', self.cards)
        while True:
            try:
                response = input(f'Please select the index of the card you would like to play: (Trump color is {trump_color if trump_color else "any"}) ')
                if response in ['e', 'q', 'exit', 'esc']:
                    exit(1)
                card = self.cards[int(response)]
                assert card in self.valid_cards(current_trick)
                self.cards.remove(card)
                if card == 'tigress-':
                    while card not in ['pirate-', 'pass-']:
                        print('Would you like to play "pirate-" or "pass-"?')
                        card = input('Would you like to play "pirate-" or "pass-"? ')
                try:
                    return Card(card)
                except:
                    print('Not a valid option.')
            except (ValueError, IndexError):
                print('Not a valid index.')
            except AssertionError:
                print('You must follow suit or play a special card.')


    def bet(self, number_of_players:int):
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
    def play(self, current_trick:list, trump_color:str, number_of_players:int = 0) -> str:
        if len(self.cards) == 1:
            return self.cards.pop()
        valid_card_list = self.valid_cards(current_trick)
        card = choice(valid_card_list)
        self.cards.remove(card)
        if card == 'tigress-':
            card = Card('pirate-' if random() >= 0.5 else 'pass-')
        return card

    def try2win(self, current_trick:list[Card], trump_color:str):
        winners = set(self.cards) & set(winning_special)
        for card in winners:
            if card == Game.winning_card(current_trick):
                continue
            elif card == Game.winning_card(current_trick+[card]):
                return card

        for card in [card for card in self.cards if card.color == 'black']:
            if card == Game.winning_card(current_trick):
                continue
            elif card == Game.winning_card(current_trick+[card]):
                return card

        if card := self.card_in_color(trump_color, best=False):
            return card

        for card in self.cards:
            if card == Game.winning_card(current_trick):
                continue
            elif card == Game.winning_card(current_trick+[card]):
                return card
        return self.cards[0]

    def try2lose(self, current_trick:list, trump_color:str):
        if len(current_trick) == 0:
            non_winning = set(self.cards) - set(winning_special)
            if len(non_winning) > 0:
                return sorted(non_winning, key=lambda x: x.number)[0]
            return self.cards[0]
        winning_card = Game.winning_card(current_trick)
        if 'white_whale-' in current_trick and winning_card:
            if 'skullking-' in self.cards:
                return Card('skullking-')
            elif 'pirate-' in self.cards:
                return Card('pirate-')
            elif 'mermaid-' in self.cards:
                return Card('mermaid-')
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
        if 'kraken-' in current_trick and winning_card:
            if 'skullking-' in self.cards:
                return Card('skullking-')
            elif 'pirate-' in self.cards:
                return Card('pirate-')
            elif 'mermaid-' in self.cards:
                return Card('mermaid-')
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
            if card == Game.winning_card(current_trick):
                return card
            elif card != Game.winning_card(current_trick+[card]):
                return card
        return card

    def card_in_color(self, color, best=True, max_value=14, min_value=1):
        candidate = ''
        for card in sorted(self.cards, key=lambda x: x.number, reverse=not best):
            if card.color == color:
                if not candidate:
                    candidate = card
                elif (candidate.number < card.number < max_value) if best else (min_value < card.number < candidate.number):
                    candidate = card
        return candidate

    def bet(self, number_of_players:int):
        card_colors = [card.split('-')[0] for card in self.cards]
        bet = card_colors.count('skullking') + card_colors.count('pirate') + card_colors.count('mermaid') + card_colors.count('black') // 2
        self.current_bet = bet
        return bet  # random.randint(0, min(len(self.cards), 4))

# class Vision(CPU):
#     def look_at_card(self) -> None:
#         card = identify_card()
#         self.add_card(Card(card))


# class AI(CPU):
#   pass
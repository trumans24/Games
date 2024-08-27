from  pandas import DataFrame, Categorical
from random import shuffle
from cards import deck, Card
from numpy import array, nan


class Game:
    def __init__(self, deck: list, playerDict: dict, human=False) -> None:
        self.trump = ''
        self.round = 1
        self.trick = 1
        self.cards = deck
        self.playerDict = playerDict
        self.playerNames = list(self.playerDict.keys())
        self.number_of_players = len(self.playerNames)
        self.human_Playing = human

    def reset(self):
        self.trump = ''
        self.round = 1
        self.trick = 1
        self.cards = deck
        for player in self.playerDict.values():
            player.cards = []
            player.current_bet = 0
            player.tricks_won = 0

    def deal(self, n=0):
        deck = self.cards.copy()
        shuffle(deck)
        for _ in range(n) if n else range(self.round):
            for _, player in self.playerDict.items():
                player.add_card(deck.pop())

    def new_game(self):
        self.reset()
        scores = {name: 0 for name, player in self.playerDict.items()}
        while self.round <= 10:
            self.deal()
            bets = self.play_round()
            for name in scores:
                if bets[name][0] == bets[name][1]:
                    scores[name] += 20 * bets[name][0] if bets[name][0] else 10 * self.round
                else:
                    scores[name] -= 10 * abs(bets[name][0] - bets[name][1]) if bets[name][0] else 10 * self.round
            if self.human_Playing:
                print('_'*100)
                print(f'The Scores after round {self.round}:')
                print(scores)
            self.round += 1
        return scores

    def play_round(self):
        bets = {name: [player.bet(len(self.playerDict)), 0] for name, player in self.playerDict.items()}
        if self.human_Playing:
            print('_'*100)
            print(f'The bets for round {self.round}:')
            print(bets)
        _ = next(playerIter := iter(self.playerDict))
        next_player_name = next(playerIter)
        for _ in range(self.round):
            self.trump = ''
            winner = self.play_trick()
            if winner in bets:
                bets[winner][1] += 1
                self.playerDict[winner].tricks_won += 1
        if self.human_Playing:
            print(bets)
        self.reorder_players(next_player_name)
        return bets

    def play_trick(self):
        cards = []
        for _, player in self.playerDict.items():
            card = player.play(cards, self.trump)
            cards.append(card)
            if not self.trump:
                self.trump = self.get_trump_color(cards)
        if 'kraken-' in cards:
            kraken_index = cards.index('kraken-')
            first_player, *other_players = self.playerDict.keys()
            other_players.append(first_player)
            next_player = other_players[kraken_index]
            self.reorder_players(next_player)
            if self.human_Playing:
                print(f'The Kraken was played. {next_player} will start the next round.')
            return ''
        else:
            winner = list(self.playerDict)[cards.index(self.winning_card(cards))]
            self.reorder_players(winner)
            if self.human_Playing:
                print(f'The winner of the round is {winner} by playing a {self.winning_card(cards)}')
            return winner

    def reorder_players(self, starting_player_name):
        playerList = list(self.playerDict.values())
        starting_index = playerList.index(self.playerDict[starting_player_name])
        self.playerDict = {player.name: player for player in playerList[starting_index:] + playerList[:starting_index]}

    @staticmethod
    def get_trump_color(cards):
        for card in cards:
            if card.color in ["black","purple","green","yellow"]:
                return card.color
            elif card.color in ['skullking', 'pirate', 'mermaid', 'white_whale', 'kraken']:
                return "any"
        return ""

    @staticmethod
    def rank_cards(cards):
        df = DataFrame({'color':card.split('-')[0], 'number':int(card.split('-')[1]) if card.split('-')[1] else nan} for card in cards)
        regular_colors = set(df.query('color in ["purple","green","yellow"]')['color'])
        color_list = df['color'].to_list()
        if 'white_whale' in color_list:
            return df.sort_values(by=['number'], ascending=False)
        # if 'kraken' in color_list:
        #     return
        elif 'skullking' in color_list and 'mermaid' in color_list[color_list.index('skullking'):]:
            special_color = ['mermaid', 'skullking', 'pirate', 'black']
            color_order = special_color + list(regular_colors) + ['pass', 'tigress', 'kraken']
        else:
            special_color = ['skullking', 'pirate', 'mermaid', 'black']
            color_order = special_color + list(regular_colors) + ['pass', 'tigress', 'kraken']
        df['color'] = Categorical(df['color'], color_order)
        sorted_trick = df.sort_values(by=['number'], ascending=False).sort_values(by='color')
        return sorted_trick

    @staticmethod
    def winning_card(cards):
        if len(cards) < 1:
            return ''
        if 'white_whale-' in cards:
            card_numbers = [card.number for card in cards]
            return cards[array(card_numbers).argmax()]
        elif 'kraken-' in cards:
            return ''
        elif 'skullking-' in cards:
            if 'mermaid-' in cards and cards.index('mermaid-') > cards.index('skullking-'):
                return Card('mermaid-')
            return 'skullking-'
        elif 'pirate-' in cards:
            return Card('pirate-')
        elif 'mermaid-' in cards:
            return Card('mermaid-')
        for card in cards:
            if not (hasattr(card, 'color') and hasattr(card, 'number'))          :
              print(card)
            assert hasattr(card, 'color') and hasattr(card, 'number')
        trump_color = 'black' if 'black' in ''.join(cards) else Game.get_trump_color(cards)
        card_numbers = [card.number if card.color == trump_color else 0 for card in cards]
        return cards[array(card_numbers).argmax()]



import requests

class OnlineGame(Game):
    def __init__(self, deck: list, playerDict: dict, host='http://127.0.0.1:8000', game_id=0, human=False) -> None:
        super().__init__(deck, playerDict, human)
        self.host = host
        self.game_id = game_id
        # self.new_deck(deck)

    def reset(self):
        self.trump = ''
        self.round = 1
        self.trick = 1
        self.new_deck(self.cards)
        for player in self.playerDict.values():
            player.cards = []
            player.current_bet = 0
            player.tricks_won = 0

    def deal(self, n=0):
        self.new_deck(self.cards)
        for _ in range(n) if n else range(self.round):
            for _, player in self.playerDict.items():
                card = self.draw()['card']
                if card is not None:
                    player.add_card(Card(card))

    # def play_round(self):
    #     return super().play_round()

    def new_deck(self, deck):
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        json_data = {
            'deck': deck,
        }

        return requests.post(f'{self.host}/{self.game_id}/new-deck', headers=headers, json=json_data)

    def draw(self):
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
        }
        r = requests.get(f'{self.host}/{self.game_id}/deal', headers=headers)
        return r.json()

from  pandas import DataFrame, Categorical
from random import shuffle
from skullking.cards import deck, Card
from numpy import array, nan
from typing import *


class Game:
    def __init__(self, deck: List, playerDict: Dict, human=False) -> None:
        self.trump = ''
        self.round = 1
        self.trick = 1
        self.cards = deck
        self.playerDict = playerDict
        self.number_of_players = len(self.playerNames)
        self.human_playing = human

    @property
    def playerNames(self):
        return list(self.playerDict.keys())
    
    def print_game(self, title: str, stats: Dict, message: str) -> None:
        stat_string = '\n'.join(f"{player_name}: {score}" for player_name, score in stats.items())
        """
        Displayes a the current state of the game
        args:
        scores - displays the current player scores
        message - display a custom message
        """
        formated_game = '''
====================================
ROUND {round}
Player {title}:
{players}
------------------------------------
{message}
===================================='''
        print(formated_game.format(round=self.round, title=title, players=stat_string, message=message))

    def reset(self) -> None:
        """
        Reset the game to its initial state.
        
        Resets trump color, round/trick counters, deck, and all player states.
        Clears all player cards, bets, and tricks won.
        """
        self.trump = ''
        self.round = 1
        self.trick = 1
        self.cards = deck
        for player in self.playerDict.values():
            player.cards = []
            player.current_bet = 0
            player.tricks_won = 0

    def deal(self, n: int = 0) -> None:
        """
        Deal cards to all players.
        
        Args:
            n (int, optional): Number of cards to deal per player. 
                              If 0, deals cards equal to current round number.
        
        Creates a shuffled copy of the deck and deals cards to each player.
        """
        deck = self.cards.copy()
        shuffle(deck)
        for _ in range(n) if n else range(self.round):
            for _, player in self.playerDict.items():
                player.add_card(deck.pop())

    def new_game(self) -> dict:
        """
        Play a complete Skull King game (10 rounds).
        
        Returns:
            dict: Final scores for all players
            
        Game flow:
        1. Reset game state
        2. Play 10 rounds (1-10 cards per round)
        3. Calculate scores based on bet accuracy
        4. Return final scores
        """
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
            if self.human_playing:
                # print('_'*100)
                # print(f'The Scores after round {self.round}:')
                # print(scores)
                self.print_game('Scores', scores, '')
            self.round += 1
        return scores

    def play_round(self) -> dict:
        """
        Play a complete round of Skull King.
        
        Returns:
            dict: Dictionary with bet results for each player
                 Format: {player_name: [bet_made, tricks_won]}
        
        Round flow:
        1. Collect bets from all players
        2. Play tricks equal to round number
        3. Track tricks won by each player
        4. Reorder players for next round
        """
        bets = {name: [player.bet(len(self.playerDict)), 0] for name, player in self.playerDict.items()}
        if self.human_playing:
            
            self.print_game('Bets', bets, 'Beginning of the round')
            # print('_'*100)
            # print(f'The bets for round {self.round}:')
            # print(bets)
        _ = next(playerIter := iter(self.playerDict))
        next_player_name = next(playerIter)
        for _ in range(self.round):
            self.trump = ''
            winner = self.play_trick()
            if winner in bets:
                bets[winner][1] += 1
                self.playerDict[winner].tricks_won += 1
        if self.human_playing:
            self.print_game('Bets', bets, 'End of the round')
        self.reorder_players(next_player_name)
        return bets

    def play_trick(self) -> str:
        """
        Play a single trick in the current round.
        
        Returns:
            str: Name of the winning player, or empty string if Kraken was played
        
        Trick flow:
        1. Each player plays a card in turn
        2. First card determines trump color
        3. Special handling for Kraken card
        4. Determine winner based on card hierarchy
        5. Reorder players for next trick
        """
        cards = []
        cards_dict = {}
        for player_name, player in self.playerDict.items():
            card = player.play(cards_dict, self.trump)
            cards.append(card)
            cards_dict[player_name] = card
            if not self.trump:
                self.trump = self.get_trump_color(cards)
        if 'kraken' in cards:
            kraken_index = cards.index('kraken')
            first_player, *other_players = self.playerDict.keys()
            other_players.append(first_player)
            next_player = other_players[kraken_index]
            self.reorder_players(next_player)
            if self.human_playing:
                self.print_game('Cards', cards_dict, f'The Kraken was played. {next_player} will start the next round.')
                # print(f'The Kraken was played. {next_player} will start the next round.')
            return ''
        else:
            winner = self.playerNames[cards.index(self.winning_card(cards))]
            self.reorder_players(winner)
            if self.human_playing:
                # print(f'The winner of the round is {winner} by playing a {self.winning_card(cards)}')
                self.print_game('Cards', cards_dict, f'The winner of the round is {winner} by playing a {self.winning_card(cards)}')
            return winner

    def reorder_players(self, starting_player_name: str) -> None:
        """
        Reorder the player dictionary so the specified player goes first.
        
        Args:
            starting_player_name (str): Name of the player who should start next
        
        Reorders the playerDict so that the specified player becomes the first
        in the turn order for subsequent tricks/rounds.
        """
        playerList = list(self.playerDict.values())
        starting_index = playerList.index(self.playerDict[starting_player_name])
        self.playerDict = {player.name: player for player in playerList[starting_index:] + playerList[:starting_index]}

    @staticmethod
    def get_trump_color(cards: Iterable[Card]) -> str:
        for card in cards:
            if card.color in ["black","purple","green","yellow"]:
                return card.color
            elif card.color in ['skullking', 'pirate', 'mermaid', 'white_whale', 'kraken']:
                return "any"
        return ""

    # @staticmethod
    # def rank_cards(cards):
    #     df = DataFrame({'color':card.color, 'number': card.number} for card in cards)
    #     regular_colors = set(df.query('color in ["purple","green","yellow"]')['color'])
    #     color_list = df['color'].to_list()
    #     if 'white_whale' in color_list:
    #         return df.sort_values(by=['number'], ascending=False)
    #     # if 'kraken' in color_list:
    #     #     return
    #     elif 'skullking' in color_list and 'mermaid' in color_list[color_list.index('skullking'):]:
    #         special_color = ['mermaid', 'skullking', 'pirate', 'black']
    #         color_order = special_color + list(regular_colors) + ['pass', 'tigress', 'kraken']
    #     else:
    #         special_color = ['skullking', 'pirate', 'mermaid', 'black']
    #         color_order = special_color + list(regular_colors) + ['pass', 'tigress', 'kraken']
    #     df['color'] = Categorical(df['color'], color_order)
    #     sorted_trick = df.sort_values(by=['number'], ascending=False).sort_values(by='color')
    #     return sorted_trick

    @staticmethod
    def winning_card(cards: List[Card]) -> Card | None:
        if len(cards) < 1:
            return None
        if 'white_whale' in cards:
            return cards[array([card.number for card in cards if card.number <= 14]).argmax()]
        elif 'kraken' in cards:
            return None
        elif 'skullking' in cards:
            if 'mermaid' in cards and cards.index(Card('mermaid')) > cards.index(Card('skullking')):
                return Card('mermaid')
            return Card('skullking')
        elif 'pirate' in cards:
            return Card('pirate')
        elif 'mermaid' in cards:
            return Card('mermaid')
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
        """
        Initialize an online Skull King game with remote deck management.
        
        Args:
            deck (list): List of cards in the game deck
            playerDict (dict): Dictionary mapping player names to Player objects
            host (str, optional): API host URL. Defaults to 'http://127.0.0.1:8000'.
            game_id (int, optional): Unique game identifier. Defaults to 0.
            human (bool, optional): Whether a human is playing. Defaults to False.
        
        Attributes:
            host (str): API server host URL
            game_id (int): Unique identifier for this game session
        """
        super().__init__(deck, playerDict, human)
        self.host = host
        self.game_id = game_id
        # self.new_deck(deck)

    def reset(self):
        """
        Reset the online game to its initial state.
        
        Resets trump color, round/trick counters, creates new deck via API,
        and clears all player states.
        """
        self.trump = ''
        self.round = 1
        self.trick = 1
        self.new_deck(self.cards)
        for player in self.playerDict.values():
            player.cards = []
            player.current_bet = 0
            player.tricks_won = 0

    def deal(self, n: int = 0) -> None:
        """
        Deal cards to all players using remote API.
        
        Args:
            n (int, optional): Number of cards to deal per player.
                              If 0, deals cards equal to current round number.
        
        Creates a new deck via API and draws cards for each player.
        """
        self.new_deck(self.cards)
        for _ in range(n) if n else range(self.round):
            for _, player in self.playerDict.items():
                card = self.draw()['card']
                if card is not None:
                    player.add_card(Card(card))

    # def play_round(self):
    #     return super().play_round()

    def new_deck(self, deck: list) -> requests.Response:
        """
        Create a new deck on the remote server.
        
        Args:
            deck (list): List of cards to initialize the deck with
        
        Returns:
            requests.Response: API response from the server
        
        Sends a POST request to create a new deck on the remote server.
        """
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        json_data = {
            'deck': deck,
        }

        return requests.post(f'{self.host}/{self.game_id}/new-deck', headers=headers, json=json_data)

    def draw(self) -> dict:
        """
        Draw a card from the remote deck.
        
        Returns:
            dict: JSON response containing the drawn card
            
        Makes a GET request to the remote server to draw a single card
        from the current deck.
        """
        headers = {
            'accept': 'application/json',
            'content-type': 'application/x-www-form-urlencoded',
        }
        r = requests.get(f'{self.host}/{self.game_id}/deal', headers=headers)
        return r.json()

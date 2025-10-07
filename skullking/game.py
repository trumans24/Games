from  pandas import DataFrame, Categorical
from random import shuffle
from cards import deck, Card
from numpy import array, nan


class Game:
    def __init__(self, deck: list, playerDict: dict, human=False) -> None:
        """
        Initialize a new Skull King game.
        
        Args:
            deck (list): List of cards in the game deck
            playerDict (dict): Dictionary mapping player names to Player objects
            human (bool, optional): Whether a human is playing. Defaults to False.
        
        Attributes:
            trump (str): Current trump color for the trick
            round (int): Current round number (1-10)
            trick (int): Current trick number within the round
            cards (list): List of cards in the deck
            playerDict (dict): Dictionary of players
            playerNames (list): List of player names
            number_of_players (int): Total number of players
            human_Playing (bool): Whether human is playing
        """
        self.trump: str = ''
        self.round: int = 1
        self.trick: int = 1
        self.cards: list = deck
        self.playerDict: dict = playerDict
        self.playerNames: list = list(self.playerDict.keys())
        self.number_of_players: int = len(self.playerNames)
        self.human_Playing: bool = human

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
            if self.human_Playing:
                print('_'*100)
                print(f'The Scores after round {self.round}:')
                print(scores)
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
    def get_trump_color(cards: list[Card]) -> str:
        """
        Determine the trump color from played cards.
        
        Args:
            cards (list): List of Card objects played in the trick
        
        Returns:
            str: Trump color ("black", "purple", "green", "yellow", "any", or "")
        
        Rules:
        - Regular colors (black, purple, green, yellow) set trump
        - Special cards (skullking, pirate, mermaid, white_whale, kraken) return "any"
        - Returns empty string if no trump can be determined
        """
        for card in cards:
            if card.color in ["black","purple","green","yellow"]:
                return card.color
            elif card.color in ['skullking', 'pirate', 'mermaid', 'white_whale', 'kraken']:
                return "any"
        return ""

    @staticmethod
    def rank_cards(cards: list[Card]) -> DataFrame:
        """
        Rank cards for determining trick winner.
        
        Args:
            cards (list): List of card strings in format "color-number"
        
        Returns:
            DataFrame: Sorted DataFrame with card rankings
        
        Special rules:
        - White whale: highest number wins regardless of color
        - Mermaid beats Skull King if played after
        - Special card hierarchy: mermaid > skullking > pirate > black > regular colors
        """
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
    def winning_card(cards: list[Card]) -> str:
        """
        Determine the winning card from a trick.
        
        Args:
            cards (list): List of Card objects played in the trick
        
        Returns:
            Card or str: The winning card, or empty string for special cases
        
        Winning hierarchy:
        1. White whale: highest number wins
        2. Kraken: no winner (returns empty string)
        3. Mermaid beats Skull King if played after
        4. Skull King beats other special cards
        5. Pirate beats regular cards
        6. Mermaid beats regular cards
        7. Highest trump color card wins
        """
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

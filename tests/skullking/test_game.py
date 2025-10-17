from skullking.cards import Card
from skullking.game import Game
from skullking.player import CPU, Human


class TestGameWinningCard:
    def test_winning_card_highest_numbered_card(self):
        winning_card = 'black-14'
        cards = [Card('yellow-5'), Card('black-14'), Card('black-12'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
        assert Game.winning_card(cards) == winning_card

    def test_winning_card_kraken_nullifies(self):
        winning_card = None
        cards = [Card('yellow-5'), Card('black-14'), Card('black-12'), Card('black-13'), Card('green-13'), Card('kraken'), Card('yellow-6')]
        assert Game.winning_card(cards) == winning_card

    def test_winning_card_pirate_wins(self):
        winning_card = 'pirate'
        cards = [Card('yellow-5'), Card('black-14'), Card('pirate'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
        assert Game.winning_card(cards) == winning_card

    def test_winning_card_mermaid_wins(self):
        winning_card = 'mermaid'
        cards = [Card('yellow-5'), Card('black-14'), Card('mermaid'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
        assert Game.winning_card(cards) == winning_card

    def test_winning_card_skullking_wins(self):
        winning_card = 'skullking'
        cards = [Card('yellow-5'), Card('skullking'), Card('black-12'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
        assert Game.winning_card(cards) == winning_card

    def test_winning_card_pirate_beats_numbered_with_white_whale(self):
        winning_card = 'black-14'
        cards = [Card('yellow-5'), Card('black-14'), Card('black-12'), Card('pirate'), Card('green-13'), Card('yellow-13'), Card('white_whale')]
        assert Game.winning_card(cards) == winning_card

from cards import Card
from game import Game
from player import Player, CPU, Human

winning_card = 'black-14'
cards = [Card('yellow-5'), Card('black-14'), Card('black-12'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
assert Game.winning_card(cards) == winning_card, f'Winning card was {Game.winning_card(cards)}, but it should be {'skullking'}'

# Kraken means nobody wins
winning_card = None
cards = [Card('yellow-5'), Card('black-14'), Card('black-12'), Card('black-13'), Card('green-13'), Card('kraken'), Card('yellow-6')]
assert Game.winning_card(cards) == winning_card, f'Winning card was {Game.winning_card(cards)}, but it should be {'skullking'}'

# Pirate wins
winning_card = 'pirate'
cards = [Card('yellow-5'), Card('black-14'), Card('pirate'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
assert Game.winning_card(cards) == winning_card, f'Winning card was {Game.winning_card(cards)}, but it should be {'skullking'}'

# Mermaid wins
winning_card = 'mermaid'
cards = [Card('yellow-5'), Card('black-14'), Card('mermaid'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
assert Game.winning_card(cards) == winning_card, f'Winning card was {Game.winning_card(cards)}, but it should be {'skullking'}'


winning_card = 'skullking'
cards = [Card('yellow-5'), Card('skullking'), Card('black-12'), Card('black-13'), Card('green-13'), Card('yellow-13'), Card('yellow-6')]
assert Game.winning_card(cards) == winning_card, f'Winning card was {Game.winning_card(cards)}, but it should be {'skullking'}'

winning_card = 'black-14'
cards = [Card('yellow-5'), Card('black-14'), Card('black-12'), Card('pirate'), Card('green-13'), Card('yellow-13'), Card('white_whale')]
assert Game.winning_card(cards) == winning_card, f'Winning card was {Game.winning_card(cards)}, but it should be {'skullking'}'


current_trick = {
    CPU('Taylor'): Card('green-11'),
    CPU('Alex'): Card('green-6'),
    CPU('Taylor2'): Card('purple-2'),
    CPU('Alex2'): Card('pirate'),
    CPU('Taylor3'): Card('purple-10'),
    Human('Alex3'): Card('black-2'),
}
sam = Human('Sam', [Card('skullking')])
card = sam.play(current_trick, trump_color='green')
assert 'skullking' == card



print('All tests have passed.')
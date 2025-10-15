from game import Game
from player import CPU, Human
from cards import deck

players = {
    'Taylor': CPU('Taylor'),
    'Alex': CPU('Alex'),
    'Taylor2': CPU('Taylor2'),
    'Alex2': CPU('Alex2'),
    'Taylor3': CPU('Taylor3'),
    'Alex3': CPU('Alex3'),
    'Sam': Human('Sam')
}

game = Game(deck, players, human=True)

print(game.new_game())

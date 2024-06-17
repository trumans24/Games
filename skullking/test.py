from game import Game
from player import CPU, Human
from cards import deck

players = {
    'Taylor': CPU('Taylor'),
    'Alex': CPU('Alex'),
    'Sam': Human('Sam')
}
game = Game(deck, players, human=True)

game.new_game()

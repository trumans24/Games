from typing import Dict


game_string = \
'''====================================
{title}:
{stats}
------------------------------------
{message}
===================================='''

def print_game(title: str = '', stats: Dict = {}, message: str = '') -> None:
        """
        Displays a the current state of the game
        args:
        round - displays the current round number
        title - displays the title of the current game state
        scores - displays the current player scores
        message - display a custom message
        """
        stat_string = '\n'.join(f"{player_name}: {score}" for player_name, score in stats.items())
        print(game_string.format(title=title, stats=stat_string, message=message))

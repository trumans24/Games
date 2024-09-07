import os
import time
from util import play_game, roll_dice, highest_score, play_round
# os.system('cls' if os.name == 'nt' else "printf '\033c'")
game_state = dict(
    player_score=0,
    computer_score=0,
    player_last_score=0,
    computer_last_score=0,
    dice=[0,0,0,0,0,0],
    number_of_dice=6,
    message='',
    response='start',
)

game_state_string = """
________Total Scores_____________________
Your score: {player_score:>26}
Computer score: {computer_score:>22}
_________________________________________
Your score this round: {player_last_score:>16}
Computer's score this round: {computer_last_score:>10}
-----------------------------------------
Your current {number_of_dice} dice:
{dice}
{message}
"""

while game_state['response']:
    game_state['player_last_score'] = 0
    game_state['computer_last_score'] = 0

    game_state['computer_last_score'] = play_round()
    game_state['computer_score'] += game_state['computer_last_score']
    while game_state['response'] != 'stop' and game_state['response']:
        # print()
        game_state['dice'] = sorted(roll_dice(game_state['number_of_dice']))
        game_state['message'] = 'What is your score? '
        
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(game_state_string.format(**game_state), end='')
        game_state['response'] = input()
        if game_state['response'] == '0' or not game_state['response']:
            game_state['number_of_dice'] = 6
            game_state['player_last_score'] = 0
            break
        game_state['player_last_score'] += int(game_state['response']) if game_state['response'].isdigit() else 0

        
        game_state['message'] = 'How many dice would you like to re-roll? '
        
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print(game_state_string.format(**game_state), end='')
        game_state['response'] = input()
        if game_state['response'] == '0' or not game_state['response']:
            game_state['number_of_dice'] = 6
            game_state['response'] = 'next_round'
            break
        game_state['number_of_dice'] = int(game_state['response']) if game_state['response'].isdigit() else 6
    game_state['player_score'] += game_state['player_last_score']
    
    if game_state['player_score'] >= 10_000 or game_state['computer_score'] >= 10_000:
        if game_state['player_score'] > game_state['computer_score']:
            print('Congradulations You WIN!!!!!')
        elif game_state['player_score'] < game_state['computer_score']:
            print('Better luck next time')
        else:
            print('Congradulations You and the Computer tied!')
        break



# print(game_state.format(player_score=100, score = 100))
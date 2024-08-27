from collections import namedtuple, deque
from torchvision import transforms
from itertools import product, count
from tqdm import tqdm

import plotly.express as px
import pandas as pd
import numpy as np
import random
import math
import cv2

import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
import torch

num2card = {0: 'skullking-',1: 'pirate-',2: 'mermaid-',3: 'tigress-',4: 'black-14',5: 'black-13',6: 'black-12',7: 'black-11',8: 'black-10',9: 'black-9',10: 'black-8',11: 'black-7',12: 'black-6',13: 'black-5',14: 'black-4',15: 'black-3',16: 'black-2',17: 'black-1',18: 'yellow-14',19: 'yellow-13',20: 'yellow-12',21: 'yellow-11',22: 'yellow-10',23: 'yellow-9',24: 'yellow-8',25: 'yellow-7',26: 'yellow-6',27: 'yellow-5',28: 'yellow-4',29: 'yellow-3',30: 'yellow-2',31: 'yellow-1',32: 'green-14',33: 'green-13',34: 'green-12',35: 'green-11',36: 'green-10',37: 'green-9',38: 'green-8',39: 'green-7',40: 'green-6',41: 'green-5',42: 'green-4',43: 'green-3',44: 'green-2',45: 'green-1',46: 'purple-14',47: 'purple-13',48: 'purple-12',49: 'purple-11',50: 'purple-10',51: 'purple-9',52: 'purple-8',53: 'purple-7',54: 'purple-6',55: 'purple-5',56: 'purple-4',57: 'purple-3',58: 'purple-2',59: 'purple-1',60: 'pass-',61: 'white_whale-',62: 'kraken-',63: 'mermaid- (2)',64: 'pirate- (2)',65: 'pirate- (3)',66: 'pirate- (4)',67: 'pirate- (5)'}
cv2_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
model = torch.load(r'C:\Users\truma\Projects\Games\model.pt',map_location=torch.device('cpu'))
_ = model.eval()
def identify_card(show=False, blur=True):
    vid = cv2.VideoCapture(0)
    while(True): 
        ret, frame = vid.read()
        top_left = (200, 200)
        bottom_right = (424, 424)
        torch_img = cv2_transform(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)[top_left[0]:bottom_right[0], top_left[1]:bottom_right[1]])
        out = model(torch_img.unsqueeze(0)).softmax(-1)
        index = out.argmax().item()
        card = num2card[index]
        confidence = out[0][index]
        cv2.rectangle(frame,top_left, bottom_right, 255, 2)
        show_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if blur:
            show_img = cv2.blur(show_img, (20, 20))
        if show:
            cv2.imshow('frame', show_img)
            cv2.setWindowTitle('frame', f'Prediction: {card}, confidence: {confidence}, counter: {0}')
        if confidence > 0.9:
            cv2.waitKey(10)
            break
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
    cv2.waitKey(10)
    vid.release()
    cv2.waitKey(10)
    cv2.destroyAllWindows()
    cv2.waitKey(10)
    return card.split()[0]

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
card_value_dict = {
    'skullking':17,
    'pirate': 16,
    'mermaid': 15,
}
class Card(str):
    def __new__(cls, value):
        obj = str.__new__(cls, value)
        color, number = obj.split('-')
        obj.color = color
        obj.number = int(number) if number else (card_value_dict[color] if color in card_value_dict else 0)
        return obj

colors = 'black', 'yellow', 'green', 'purple'
numbers = tuple(range(14,0, -1))
winning_special = ['skullking-'] + ['pirate-']*5 + ['mermaid-']*2 + ['tigress-']
winning_special = [Card(card) for card in winning_special]
lossing_special = ['pass-']*5+ ['white_whale-'] + ['kraken-'] + ['tigress-']
lossing_special = [Card(card) for card in lossing_special]

special = winning_special + lossing_special
special.remove('tigress-')
deck = special + ['-'.join([color, str(number)]) for color, number in product(colors, numbers)]
deck = [Card(card) for card in deck]
available_cards = ['skullking-', 'pirate-', 'mermaid-', 'tigress-'] + ['-'.join([color, str(number)]) for color, number in product(colors, numbers)] + ['pass-', 'white_whale-', 'kraken-']
available_cards = [Card(card) for card in available_cards]
deckDict = dict(zip(available_cards, range(len(available_cards))))

def cards2vect(number_of_players, cards):
    card_vector = torch.zeros(len(deckDict))
    for card in cards:
        card_vector[deckDict[card]] += 1.0
    return torch.concat([torch.tensor([number_of_players]), card_vector])

def vect2cards(vect):
    return [available_cards[i] for i, card in enumerate(vect) if card > 0]

def state2cards(state):
  flat_state = state.squeeze()
  number_of_players = flat_state[0]
  a = flat_state[1:len(flat_state)//2]
  b = flat_state[len(flat_state)//2+1:]
  cards = vect2cards(a)
  hand = vect2cards(b)
  return number_of_players.item(), cards, hand


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
        print('Cards that have already been played in this trick:', current_trick if len(current_trick) > 0 else None)
        print('What card would you like to pley? Cards in hand:', self.cards)
        while True:
            try:
                card = self.cards[int(input(f'Please select the index of the card you would like to play: (Trump color is {trump_color})'))]
                assert card in self.valid_cards(current_trick)
                self.cards.remove(card)
                if card == 'tigress-':
                    while card not in ['pirate-', 'pass-']:
                        print('Would you like to play "pirate-" or "pass-"?')
                        card = input('Would you like to play "pirate-" or "pass-"?')
                return card
            except:
                print('Not a valid index.')


    def bet(self, number_of_players:int):
        print('Please make your bet. Cards in hand:', self.cards)
        while True:
            try:
                return int(input(f'What would you like to bet? (Max bet is {len(self.cards)})'))
            except:
                print('Not a valid bet.')

class CPU(Player):
    def play(self, current_trick:list, trump_color:str, number_of_players:int = 0) -> str:
        if len(self.cards) == 1:
            return self.cards.pop()
        valid_card_list = self.valid_cards(current_trick)
        card = random.choice(valid_card_list)
        self.cards.remove(card)
        if card == 'tigress-':
            card = Card('pirate-' if random.random() >= 0.5 else 'pass-')
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

class Vision(CPU):
    def look_at_card(self) -> None:
        card = identify_card()
        self.add_card(Card(card))
# model = nn.Sequential(
#     nn.Linear(in_features=64, out_features=1),
# )

# model.load_state_dict(torch.load('data/model_state.pt'))
class AI(CPU):
  pass
    # def bet(self, number_of_players:int):
    #     bet = model(cards2vect(number_of_players, self.cards)).item()
    #     return max(0, np.round(bet))  # random.randint(0, min(len(self.cards), 4))

class Game:
    def __init__(self, deck: list, playerDict: dict) -> None:
        self.trump = ''
        self.round = 1
        self.trick = 1
        self.cards = deck
        self.playerDict = playerDict
        self.playerNames = list(self.playerDict.keys())
        self.number_of_players = len(self.playerNames)
        self.human_Playing = False
        for player in playerDict:
            if isinstance(playerDict[player], Human):
                self.human_Playing = True

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
        random.shuffle(deck)
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
            self.round += 1
        return scores

    def play_round(self):
        bets = {name: [player.bet(len(self.playerDict)), 0] for name, player in self.playerDict.items()}
        _ = next(playerIter := iter(self.playerDict))
        next_player_name = next(playerIter)
        for _ in range(self.round):
            self.trump = ''
            winner = self.play_trick()
            if winner in bets:
                bets[winner][1] += 1
                self.playerDict[winner].tricks_won += 1
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
        df = pd.DataFrame({'color':card.split('-')[0], 'number':int(card.split('-')[1]) if card.split('-')[1] else np.nan} for card in cards)
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
        df['color'] = pd.Categorical(df['color'], color_order)
        sorted_trick = df.sort_values(by=['number'], ascending=False).sort_values(by='color')
        return sorted_trick

    @staticmethod
    def winning_card(cards):
        if len(cards) < 1:
            return ''
        if 'white_whale-' in cards:
            card_numbers = [card.number for card in cards]
            return cards[np.array(card_numbers).argmax()]
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
        return cards[np.array(card_numbers).argmax()]

def cards2vect(number_of_players, cards):
    card_vector = torch.zeros(len(deckDict))
    for card in cards:
        card_vector[deckDict[card]] += 1.0
    return torch.concat([torch.tensor([number_of_players]), card_vector])


def train_betting_model():
    players = [
    Tim := AI('tim'),
    Mia := AI('mia'),
    Spencer := AI('Spencer'),
    Ann := AI('ann'),
    Tom := AI('tom'),
    Cerise := CPU('Cerise'),
    ]

    model = nn.Sequential(
        nn.Linear(in_features=64, out_features=1),
    )

    optimizer = torch.optim.Adam(model.parameters())
    scheduler = torch.optim.lr_scheduler.ExponentialLR(optimizer, gamma=0.9)

    random.shuffle(players)
    game = Game(deck, {player.name: player for player in random.sample(players,random.randint(3, len(players)))})

    best_value = 0
    ave_loss = 0
    ave_accuracy = 0
    losses = []
    accuracy = []
    loss = nn.MSELoss()
    training_step = 10000
    print_step = training_step // 10 if training_step // 10 else 1
    for i in tqdm(range(1, training_step+1)):
        game = Game(deck, {player.name: player for player in random.sample(players,random.randint(3, len(players)))})
        game.round = random.randint(1, 10)
        game.deal()
        bet = torch.concat([model(cards2vect(len(game.playerDict), player.cards)) for player in game.playerDict.values()])
        actual_bets = game.play_round()
        actual = torch.tensor([player_bets[1] for player_bets in actual_bets.values()]).float()
        # print(bet, actual)
        output = loss(bet, actual)
        # correct = (bet.round() == actual).sum()
        # print(correct)
        optimizer.zero_grad()
        output.backward()
        optimizer.step()

        correct = (bet.round() == actual).sum() / len(game.playerDict)
        current_value = correct
        if current_value >= best_value:
            last_best = 0
            best_value = current_value
            best_state = {
                'epoch': i,
                'model': model.state_dict(),
                'optimizer': optimizer.state_dict(),
                'train_metrics': correct,
            }
        else:
            last_best += 1

        ave_loss += output.item()
        ave_accuracy += correct
        if i % print_step == 0:

            scheduler.step()
            print(f'Training Step #{i}: Loss={ave_loss/print_step:.3e}, Acc={ave_accuracy/print_step}')
            losses.append(ave_loss/print_step)
            accuracy.append(ave_accuracy/print_step)
            if ave_accuracy/len(game.playerDict)/print_step > 0.9:
                break
            ave_loss = 0
            ave_accuracy = 0
    a = {card: model(cards2vect(len(game.playerDict), [card])).item() for card in available_cards}
    px.scatter(x=a.keys(), y=a.values()).show()
    px.line(accuracy)
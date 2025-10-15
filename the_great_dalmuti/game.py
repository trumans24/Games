from ast import Tuple
from random import shuffle
from player import Player
from game_state import GameState
from typing import List, Dict, Self, Tuple


def get_cards(shuffle_cards=True):
  cards = []
  for i in range(1, 13):
    cards.extend([i] * i)
  cards += [13, 13]
  if shuffle_cards:
    shuffle(cards)
  return cards


class Game:
  def __init__(self, players: List[Player]) -> None:
    self.players = players
    self.cards = get_cards()
    self.game_state = GameState()
    self.num_players = len(players)

  def play(self):
    # first player trades two cards with last players
    greater_dalmutis_cards = self.players[0].give_any_cards(2)
    greater_peons_cards = self.players[-1].give_low_cards(2)
    self.players[0].add_cards(greater_peons_cards)
    self.players[-1].add_cards(greater_dalmutis_cards)
    
    # if more than 3 players, second player trades one card with the second to last player
    if len(self.players) > 3:
      lesser_dalmutis_cards = self.players[1].give_any_cards(1)
      lesser_peons_cards = self.players[-2].give_low_cards(1)
      self.players[1].add_cards(lesser_peons_cards)
      self.players[-2].add_cards(lesser_dalmutis_cards)

    last_player_to_play = self.players[0]
    finished_players = []
    
    while self.players:
      player = self.players.pop(0)
      if player == last_player_to_play:
        self.game_state.clear_current_round()
      self.game_state.add_to_current_round(player.name, player.play(self.game_state))
      print(self.game_state)
      
      if player.has_cards():
        self.players.append(player)
      else:
        finished_players.append(player)
    
    self.players = finished_players


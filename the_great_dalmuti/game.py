from random import shuffle
from the_great_dalmuti.player import Player, CPU, Human
from the_great_dalmuti.game_state import GameState
from typing import List, Dict, Self, Tuple, Sequence


def get_cards(shuffle_cards=True):
  cards = []
  for i in range(1, 13):
    cards.extend([i] * i)
  cards += [13, 13]
  if shuffle_cards:
    shuffle(cards)
  return cards


class Game:
  def __init__(self, players: List[CPU]) -> None:
    # shuffle(players)
    self.players = players
    self.cards = get_cards()
    self.game_state = GameState([p for p in players])
    self.num_players = len(players)

  def play(self):
    # Deal cards
    for i, card in enumerate(self.cards):
      self.players[i % self.num_players].add_cards(card)
    print(self.game_state)
    
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

    last_player_to_play = None
    game_over = False
    finished_players = []
    
    while self.players:
      player = self.players.pop(0)
      
      while not player.has_cards():
        finished_players.append(player)
        if not self.players:
          game_over = True
          break
        if not last_player_to_play:
          last_player_to_play = player
        elif player == last_player_to_play:
          print(f"{player.name} has won the trick but has no cards.")
          self.game_state.clear_current_round()
          if not self.players:
            break
          player = self.players.pop(0)
          print(f'{player.name}\'s turn to play.')
          last_player_to_play = player
        else:
          print(f"{player.name} has no cards, skipping turn.")
          if not self.players:
            break
          player = self.players.pop(0)
      if game_over:
        break
      
      if player == last_player_to_play:
        print(f"{player.name} has won the trick.")
        print(self.game_state)
        self.game_state.clear_current_round()
      cards_played = player.play(self.game_state)
      if cards_played:
        last_player_to_play = player
      self.game_state.add_to_current_round(player.name, cards_played)
      print(f'{player.name} played: {cards_played}')
      
      if not player.has_cards():
        print(f"{player.name} has finished all their cards!")
      
      self.players.append(player)

      response = input()
      if response in ['q', 'quit', 'exit']:
        exit(0)
      elif response in ['s', 'show']:
        for p in self.players:
          print(f"{p.name}: {p._cards}")
    
    print("Round Over! Rankings:")
    for i, player in enumerate(finished_players, 1):
        print(f"{i}. {player.name}")
    self.players = finished_players
    self.game_state = GameState(self.players.copy())


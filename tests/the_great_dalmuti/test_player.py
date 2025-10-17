from the_great_dalmuti.player import Player, CPU, Human
from the_great_dalmuti.game_state import GameState

class TestPlayer:
    def test_valid_play(self):
        player = CPU("Test")
        player.add_cards([1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 13, 13])
        game_state = GameState([player])
        
        assert player.valid_play(game_state, []) # passing
        assert (player.valid_play(game_state, [1, 2]) == False) and (player.valid_play(game_state, [1, 13]) == True) # different cards
        assert (player.valid_play(game_state, [6]) == False) and (player.valid_play(game_state, [1, 1]) == False) # cards not in hand
        game_state.add_to_current_round(player.name, [9, 9])
        game_state.add_to_current_round(player.name, [5, 5])
        game_state.add_to_current_round(player.name, [])
        assert (player.valid_play(game_state, [3, 3, 3]) == False) and (player.valid_play(game_state, [3]) == False) # wrong number of cards
        assert (player.valid_play(game_state, [6, 6]) == False) and (player.valid_play(game_state, [5, 5]) == False) and (player.valid_play(game_state, [4, 4]) == True) # not lower than last played

        game_state.clear_current_round()
        game_state.add_to_current_round(player.name, [13])
        assert player.valid_play(game_state, [5]) # last played was wild
    
    def test_get_valid_cards(self):
        player = CPU("Test")
        player.add_cards([1, 2, 2, 4, 5, 5, 5])
        assert player.get_valid_cards([6, 6]) == [2, 2, 5, 5, 5]
        assert player.get_valid_cards(None) == [1, 2, 2, 4, 5, 5, 5]
        assert player.get_valid_cards([1]) == []
        assert player.get_valid_cards([11, 11, 11]) == [5, 5, 5]
        assert player.get_valid_cards([11, 11, 11, 11]) == []

        player.add_cards([13])
        print(player.get_valid_cards([6, 6, 6]))
        assert player.get_valid_cards([6, 6, 6]) == [2, 2, 5, 5, 5, 13]

    def test_play_human(self, monkeypatch):
        inputs = iter(['', '4, 4'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        player = Human("Test")
        player.add_cards([4, 4])
        game_state = GameState([CPU('Computer1'), player])
        game_state.add_to_current_round('Computer1', [5, 5])
        assert player.play(game_state) == [] # no last played, plays highest cards
        game_state.clear_current_round()
        assert player.play(game_state) == [4, 4] # plays valid cards

    def test_play_cpu(self):
        player = CPU("Test")
        player.add_cards([1, 2, 7, 7, 10, 10, 11, 11, 11, 12, 13, 13])
        game_state = GameState([player])
        
        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)

        game_state.clear_current_round()
        game_state.add_to_current_round(player.name, [9])

        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)

        game_state.clear_current_round()
        game_state.add_to_current_round(player.name, [9, 9, 9])

        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)
        
        game_state.clear_current_round()
        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)
        
        game_state.clear_current_round()
        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)

        game_state.clear_current_round()
        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)
        
        game_state.clear_current_round()
        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)
        
        game_state.clear_current_round()
        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)

        
        player = CPU("Test")
        player2 = CPU("Test2")
        player.add_cards([10, 10, 11, 11, 11])
        player2.add_cards([3, 4, 5, 6, 8, 9, 10, 10])
        game_state = GameState([player, player2])

        cards = player.play(game_state)
        assert game_state.valid_play(cards)
        game_state.add_to_current_round(player.name, cards)
        cards2 = player2.play(game_state)
        assert game_state.valid_play(cards2)


        player1 = CPU("Test1")
        player2 = CPU("Test2")
        player3 = CPU("Test3")
        player4 = CPU("Test4")
        player1.add_cards([3, 3, 4, 4, 7, 7, 7, 7, 9, 9, 13])
        player2.add_cards([1, 2, 2, 4, 4, 5, 5, 5, 6, 6, 8, 8, 9, 10, 10, 10, 12, 12, 12, 12])
        player3.add_cards([3, 6, 6, 6, 6, 7, 8, 8, 8, 9, 9, 9, 9, 10, 10, 11, 11, 12, 12, 13])
        player4.add_cards([5, 5, 7, 7, 8, 8, 8, 9, 9, 10, 10, 10, 11, 11, 12, 12, 12, 12, 12, 12])
        game_state = GameState([player1, player2, player3, player4])
        game_state.add_to_current_round(player1.name, [10, 10])
        cards2 = player2.play(game_state)
        assert game_state.valid_play(cards2)
        game_state.add_to_current_round(player2.name, cards2)
        cards3 = player3.play(game_state)
        assert game_state.valid_play(cards3)
        game_state.add_to_current_round(player3.name, cards3)
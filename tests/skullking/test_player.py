
from skullking.cards import Card
from skullking.player import CPU, Human

class TestHumanPlay:
    def test_human_play_skullking(self, monkeypatch):
        current_trick = {
            CPU('Taylor'): Card('green-11'),
            CPU('Alex'): Card('green-6'),
            CPU('Taylor2'): Card('purple-2'),
            CPU('Alex2'): Card('pirate'),
            CPU('Taylor3'): Card('purple-10'),
            Human('Alex3'): Card('black-2'),
        }
        inputs = iter(['skullking'])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        sam = Human('Sam', [Card('skullking')])
        card = sam.play(current_trick, trump_color='green')
        assert card == 'skullking'
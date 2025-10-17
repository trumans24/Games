import argparse
from the_great_dalmuti.game import Game
from the_great_dalmuti.player import Player, CPU, Human


def parse_arguments():
    parser = argparse.ArgumentParser(description="Play The Great Dalmuti")
    parser.add_argument(
        "-n", "--num-players",
        type=int,
        default=4,
        help="Number of players (default: 4 one of which is human)"
    )
    parser.add_argument(
        "-p", "--players",
        nargs="+",
        help="Player definitions in format: name:type (e.g., 'Alice:cpu' 'Sam:human'). Type can be 'cpu' or 'human'. If not provided, defaults to 'cpu'."
    )
    return parser.parse_args()


def create_players(args):
    if args.players:
        players = []
        for player_def in args.players:
            name, *player_type = player_def.split(":")
            player_type = ''.join(player_type).lower()
            
            if player_type == "human":
                players.append(Human(name))
            else:
                players.append(CPU(name))
        return players
    else:
        # Create default players: first is Human, rest are CPU
        players = []
        for i in range(args.num_players):
            name = f"Player{i+1}"
            if i == 0:
                players.append(Human(name))
            else:
                players.append(CPU(name))
        return players


if __name__ == "__main__":
    args = parse_arguments()
    players = create_players(args)
    game = Game(players)
    while True:
        game.play()

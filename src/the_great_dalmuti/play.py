#!/usr/bin/env python3
"""CLI for The Great Dalmuti game."""
import click
from the_great_dalmuti.game import Game
from the_great_dalmuti.player import Player, CPU, CPU2, Human


@click.command()
@click.option(
    "-n", "--num-players",
    type=int,
    default=4,
    help="Number of players (default: 4, one of which is human)"
)
@click.option(
    "-p", "--players",
    multiple=True,
    help="Player definitions in format: name:type (e.g., 'Alice:cpu' 'Sam:human'). Type can be 'cpu', 'cpu2', or 'human'."
)
@click.option(
    "-q", "--quiet",
    is_flag=True,
    help="Hide game state after each turn (game state is shown by default)."
)
@click.option(
    "-g", "--num-games",
    type=int,
    default=10,
    help="Number of games to play (default: 10)."
)
def main(num_players, players, quiet, num_games):
    """Play The Great Dalmuti game."""
    if players:
        player_list = []
        for player_def in players:
            parts = player_def.split(":")
            name = parts[0]
            player_type = parts[1].lower() if len(parts) > 1 else "cpu"
            
            if player_type == "human":
                player_list.append(Human(name))
            elif player_type == "cpu2":
                player_list.append(CPU2(name))
            else:
                player_list.append(CPU(name))
    else:
        # Create default players: first is Human, rest are CPU
        player_list = []
        for i in range(num_players):
            name = f"Player{i+1}"
            if i == 0:
                player_list.append(Human(name))
            else:
                player_list.append(CPU(name))
    
    game = Game(player_list, show_print=not quiet)
    scoreboard = {}
    for _ in range(num_games):
        ranking = game.play()
        for player_name, rank in ranking.items():
            if player_name not in scoreboard:
                scoreboard[player_name] = 0
            scoreboard[player_name] += rank
    
    click.echo(f"Final Scoreboard after {num_games} games:")
    for player_name, total_rank in sorted(scoreboard.items(), key=lambda x: x[1]):
        click.echo(f"{player_name}: {total_rank}")


if __name__ == "__main__":
    main()

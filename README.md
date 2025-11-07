# ML and AI for Games

This repository is a collection of Python code and Jupyter Notebooks showcasing various projects related to card games and artificial intelligence. It explores techniques for:

- **Card Detection with Neural Networks**: Train neural networks to identify cards in images, enabling computer vision applications for card games.
- **Webcam-based Card Reading**: Utilize your webcam to capture and recognize cards in real-time, setting the stage for interactive card game experiences.
- **Game Coding Examples**: Dive into code examples for different card games, providing a foundation for building your own or implementing variations.
- **Reinforcement Learning for AI Players**: Train AI models using reinforcement learning to play card games strategically, creating intelligent opponents for your games.

## Games
### The Great Dalmuti

The Great Dalmuti is a card game where players compete to be the first to get rid of all their cards. The game uses a special deck where cards are numbered 1-13, with lower numbers appearing more frequently (1 appears once, 2 appears twice, up to 12 appearing 12 times, and 13 appearing twice as jokers).

**Game Rules:**
- Players are ranked based on their performance in the previous round
- At the start of each round, the highest-ranked player (Greater Dalmuti) trades two cards with the lowest-ranked player (Greater Peon)
- If there are more than 3 players, the second-highest player (Lesser Dalmuti) trades one card with the second-lowest player (Lesser Peon)
- Players take turns playing cards, trying to match or beat the previous play
- The first player to get rid of all their cards wins the round
- Rankings are updated after each round based on finish order

**How to Play:**

Install the package and use the `dalmuti` command to play:

**Command Options:**
- `-n, --num-players`: Number of players (default: 4, one of which is human)
- `-p, --players`: Player definitions in format `name:type` (can be used multiple times)
  - Types: `human`, `cpu`, or `cpu2`
  - Example: `-p "Alice:human" -p "Bob:cpu"`
- `-q, --quiet`: Hide game state after each turn (game state is shown by default)
- `-g, --num-games`: Number of games to play (default: 10)

```bash
# Play with default settings (4 players, 1 human + 3 CPU, 10 games)
dalmuti

# Play with a specific number of players
dalmuti -n 6

# Customize players with names and types
dalmuti -p "Alice:human" -p "Bob:cpu" -p "Charlie:cpu2" -p "Diana:cpu"

# Hide game state (game state is shown by default)
dalmuti -q

# Play a single game
dalmuti -g 1

# Combine options: play 5 games with 6 players (game state shown by default)
dalmuti -n 6 -g 5
```
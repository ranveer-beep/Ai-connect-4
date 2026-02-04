# Connect 4 AI Game

A Connect 4 game featuring an AI opponent that uses the Minimax algorithm with Alpha-Beta pruning and heuristic evaluation. The AI looks ahead 5 moves to make strategic decisions.

## Project Structure

```
AI connect 4/
├── src/
│   ├── __init__.py       # Package initialization
│   ├── main.py           # Entry point
│   ├── game.py           # Game controller
│   ├── board.py          # Board logic and game rules
│   ├── player.py         # Human player class
│   └── ai_player.py      # AI player with minimax algorithm
└── README.md
```

## Features

- **Minimax Algorithm**: AI searches 5 moves ahead
- **Alpha-Beta Pruning**: Efficient tree search optimization
- **Heuristic Evaluation**: Strategic position scoring based on:
  - Center control
  - Potential winning patterns
  - Blocking opponent threats
  - Multiple directional analysis

## How to Play

Run the game from the project root:

```bash
cd "AI connect 4/src"
python3 main.py
```

Enter column numbers (0-6) to drop your pieces. Try to connect 4 pieces horizontally, vertically, or diagonally before the AI does!

## AI Strategy

The AI evaluates positions using:
- **4 in a row**: +100 points (winning position)
- **3 in a row + 1 empty**: +5 points
- **2 in a row + 2 empty**: +2 points
- **Center control**: +3 points per piece
- **Blocking opponent's 3 in a row**: -4 points (defensive priority)

## Requirements

- Python 3.6+
- NumPy

Install dependencies:
```bash
pip install numpy
```

# Project Structure Overview

## Module Responsibilities

### 1. **main.py** - Entry Point
- Initializes and runs the game
- Single responsibility: start the application

### 2. **game.py** - Game Controller
- Manages game flow and turn logic
- Coordinates between board, players, and game state
- Handles game loop and win/draw conditions

### 3. **board.py** - Board Logic
- Manages board state (6x7 grid)
- Validates moves and checks winning conditions
- Provides heuristic evaluation for AI
- Contains all game rules

### 4. **player.py** - Human Player
- Handles user input
- Validates player moves
- Manages human player interactions

### 5. **ai_player.py** - AI Player
- Implements Minimax algorithm with Alpha-Beta pruning
- Looks ahead 5 moves
- Uses heuristic evaluation from board.py
- Makes strategic decisions

## Data Flow

```
main.py
   ↓
game.py (Game Controller)
   ↓
   ├── board.py (Board State & Rules)
   ├── player.py (Human Input)
   └── ai_player.py (AI Logic)
          ↓
       board.py (Position Evaluation)
```

## How They Interact

1. **main.py** creates a Game instance
2. **game.py** creates:
   - Board instance
   - HumanPlayer instance
   - AIPlayer instance
3. On each turn:
   - Game asks current player for a move
   - Player (human or AI) uses Board to determine valid moves
   - Board updates state and checks for win/draw
   - Game switches turns

## Running the Game

```bash
cd "AI connect 4/src"
python3 main.py
```

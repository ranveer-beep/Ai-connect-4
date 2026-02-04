"""
Connect 4 Game with AI using Minimax Algorithm with Alpha-Beta Pruning
The AI uses heuristic evaluation and looks ahead 5 moves to make strategic decisions.
"""

import numpy as np
import sys
from typing import Tuple, Optional, List

# Game Constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2

# Evaluation weights for heuristic
WINDOW_LENGTH = 4


class Connect4:
    """Connect 4 game board and logic"""

    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)
        self.game_over = False
        self.winner = None

    def is_valid_location(self, col: int) -> bool:
        """Check if a column has space for a piece"""
        return self.board[ROWS - 1][col] == EMPTY

    def get_next_open_row(self, col: int) -> int:
        """Find the next available row in a column"""
        for r in range(ROWS):
            if self.board[r][col] == EMPTY:
                return r
        return -1

    def drop_piece(self, row: int, col: int, piece: int):
        """Place a piece on the board"""
        self.board[row][col] = piece

    def get_valid_locations(self) -> List[int]:
        """Get all columns that are not full"""
        return [col for col in range(COLS) if self.is_valid_location(col)]

    def check_winner(self, piece: int) -> bool:
        """Check if a player has won"""
        # Horizontal check
        for r in range(ROWS):
            for c in range(COLS - 3):
                if all(self.board[r][c + i] == piece for i in range(4)):
                    return True

        # Vertical check
        for c in range(COLS):
            for r in range(ROWS - 3):
                if all(self.board[r + i][c] == piece for i in range(4)):
                    return True

        # Positive diagonal check
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                if all(self.board[r + i][c + i] == piece for i in range(4)):
                    return True

        # Negative diagonal check
        for r in range(3, ROWS):
            for c in range(COLS - 3):
                if all(self.board[r - i][c + i] == piece for i in range(4)):
                    return True

        return False

    def is_terminal_node(self) -> bool:
        """Check if game is over"""
        return self.check_winner(PLAYER) or self.check_winner(AI) or len(self.get_valid_locations()) == 0

    def evaluate_window(self, window: np.ndarray, piece: int) -> int:
        """Evaluate a window of 4 positions for scoring"""
        score = 0
        opp_piece = PLAYER if piece == AI else AI

        piece_count = np.count_nonzero(window == piece)
        empty_count = np.count_nonzero(window == EMPTY)
        opp_count = np.count_nonzero(window == opp_piece)

        # Strong positions
        if piece_count == 4:
            score += 100
        elif piece_count == 3 and empty_count == 1:
            score += 5
        elif piece_count == 2 and empty_count == 2:
            score += 2

        # Block opponent
        if opp_count == 3 and empty_count == 1:
            score -= 4

        return score

    def score_position(self, piece: int) -> int:
        """Heuristic evaluation of board position"""
        score = 0

        # Center column preference (center control is strategic)
        center_array = [int(i) for i in list(self.board[:, COLS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # Horizontal scoring
        for r in range(ROWS):
            row_array = [int(i) for i in list(self.board[r, :])]
            for c in range(COLS - 3):
                window = row_array[c:c + WINDOW_LENGTH]
                score += self.evaluate_window(np.array(window), piece)

        # Vertical scoring
        for c in range(COLS):
            col_array = [int(i) for i in list(self.board[:, c])]
            for r in range(ROWS - 3):
                window = col_array[r:r + WINDOW_LENGTH]
                score += self.evaluate_window(np.array(window), piece)

        # Positive diagonal scoring
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [self.board[r + i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(np.array(window), piece)

        # Negative diagonal scoring
        for r in range(ROWS - 3):
            for c in range(COLS - 3):
                window = [self.board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
                score += self.evaluate_window(np.array(window), piece)

        return score

    def print_board(self):
        """Display the board"""
        print("\n" + "=" * 29)
        print(np.flip(self.board, 0))
        print("=" * 29)
        print(" 0  1  2  3  4  5  6")
        print()


class AIPlayer:
    """AI player using Minimax with Alpha-Beta Pruning"""

    def __init__(self, depth: int = 5):
        self.depth = depth

    def minimax(self, game: Connect4, depth: int, alpha: float, beta: float,
                maximizing_player: bool) -> Tuple[Optional[int], int]:
        """
        Minimax algorithm with alpha-beta pruning
        Returns: (best_column, score)
        """
        valid_locations = game.get_valid_locations()
        is_terminal = game.is_terminal_node()

        # Base cases
        if depth == 0 or is_terminal:
            if is_terminal:
                if game.check_winner(AI):
                    return (None, 100000)
                elif game.check_winner(PLAYER):
                    return (None, -100000)
                else:  # No more valid moves
                    return (None, 0)
            else:  # Depth is zero
                return (None, game.score_position(AI))

        if maximizing_player:
            value = -np.inf
            best_col = np.random.choice(valid_locations)

            for col in valid_locations:
                row = game.get_next_open_row(col)
                temp_board = game.board.copy()

                game.drop_piece(row, col, AI)
                new_score = self.minimax(game, depth - 1, alpha, beta, False)[1]
                game.board = temp_board

                if new_score > value:
                    value = new_score
                    best_col = col

                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cutoff

            return best_col, value

        else:  # Minimizing player
            value = np.inf
            best_col = np.random.choice(valid_locations)

            for col in valid_locations:
                row = game.get_next_open_row(col)
                temp_board = game.board.copy()

                game.drop_piece(row, col, PLAYER)
                new_score = self.minimax(game, depth - 1, alpha, beta, True)[1]
                game.board = temp_board

                if new_score < value:
                    value = new_score
                    best_col = col

                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cutoff

            return best_col, value

    def get_best_move(self, game: Connect4) -> int:
        """Get the best move for AI"""
        col, score = self.minimax(game, self.depth, -np.inf, np.inf, True)
        return col


def main():
    """Main game loop"""
    game = Connect4()
    ai = AIPlayer(depth=5)
    turn = PLAYER  # Player goes first

    print("\n" + "=" * 50)
    print("        CONNECT 4 - Player vs AI")
    print("=" * 50)
    print("\nYou are Player 1 (represented by 1)")
    print("AI is Player 2 (represented by 2)")
    print("Try to connect 4 pieces horizontally, vertically, or diagonally!")
    print("\nEnter column number (0-6) to drop your piece")
    print("=" * 50)

    game.print_board()

    while not game.game_over:

        if turn == PLAYER:
            # Player's turn
            try:
                col = int(input("Your move (0-6): "))

                if col < 0 or col >= COLS:
                    print("Invalid column! Choose 0-6")
                    continue

                if not game.is_valid_location(col):
                    print("Column is full! Choose another column")
                    continue

                row = game.get_next_open_row(col)
                game.drop_piece(row, col, PLAYER)

                if game.check_winner(PLAYER):
                    game.print_board()
                    print("🎉 Congratulations! You won! 🎉")
                    game.game_over = True
                    break

            except ValueError:
                print("Invalid input! Enter a number between 0-6")
                continue
            except KeyboardInterrupt:
                print("\n\nGame terminated by user.")
                sys.exit(0)

        else:
            # AI's turn
            print("\nAI is thinking...")
            col = ai.get_best_move(game)
            row = game.get_next_open_row(col)
            game.drop_piece(row, col, AI)
            print(f"AI placed piece in column {col}")

            if game.check_winner(AI):
                game.print_board()
                print("🤖 AI wins! Better luck next time! 🤖")
                game.game_over = True
                break

        game.print_board()

        # Check for draw
        if len(game.get_valid_locations()) == 0:
            print("Game is a draw!")
            game.game_over = True
            break

        # Switch turns
        turn = AI if turn == PLAYER else PLAYER

    print("\nThanks for playing!")


if __name__ == "__main__":
    main()

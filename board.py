"""
Connect 4 Game Board
Handles board state and game logic
"""

import numpy as np
from typing import List

# Game Constants
ROWS = 6
COLS = 7
EMPTY = 0
PLAYER = 1
AI = 2
WINDOW_LENGTH = 4


class Board:
    """Connect 4 game board and logic"""

    def __init__(self):
        self.board = np.zeros((ROWS, COLS), dtype=int)

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

    def copy(self):
        """Create a deep copy of the board"""
        new_board = Board()
        new_board.board = self.board.copy()
        return new_board

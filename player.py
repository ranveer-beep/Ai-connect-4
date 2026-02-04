"""
Player classes for Connect 4
Includes Human Player and AI Player
"""

import sys
from board import Board, PLAYER, AI, COLS


class HumanPlayer:
    """Human player that takes input from console"""

    def __init__(self, piece: int):
        self.piece = piece

    def get_move(self, board: Board) -> int:
        """Get move from human player"""
        while True:
            try:
                col = int(input(f"Your move (0-{COLS-1}): "))

                if col < 0 or col >= COLS:
                    print(f"Invalid column! Choose 0-{COLS-1}")
                    continue

                if not board.is_valid_location(col):
                    print("Column is full! Choose another column")
                    continue

                return col

            except ValueError:
                print(f"Invalid input! Enter a number between 0-{COLS-1}")
                continue
            except KeyboardInterrupt:
                print("\n\nGame terminated by user.")
                sys.exit(0)

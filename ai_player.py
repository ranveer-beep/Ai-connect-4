"""
AI Player using Minimax Algorithm with Alpha-Beta Pruning
Uses heuristic evaluation and lookahead to make strategic decisions
"""

import numpy as np
from typing import Tuple, Optional
from board import Board, PLAYER, AI


class AIPlayer:
    """AI player using Minimax with Alpha-Beta Pruning"""

    def __init__(self, piece: int, depth: int = 5):
        self.piece = piece
        self.depth = depth
        self.opponent = PLAYER if piece == AI else AI

    def minimax(self, board: Board, depth: int, alpha: float, beta: float,
                maximizing_player: bool) -> Tuple[Optional[int], int]:
        """
        Minimax algorithm with alpha-beta pruning

        Args:
            board: Current game board
            depth: Remaining depth to search
            alpha: Best value for maximizer
            beta: Best value for minimizer
            maximizing_player: True if maximizing, False if minimizing

        Returns:
            Tuple of (best_column, score)
        """
        valid_locations = board.get_valid_locations()
        is_terminal = board.is_terminal_node()

        # Base cases
        if depth == 0 or is_terminal:
            if is_terminal:
                if board.check_winner(self.piece):
                    return (None, 100000)
                elif board.check_winner(self.opponent):
                    return (None, -100000)
                else:  # No more valid moves (draw)
                    return (None, 0)
            else:  # Depth is zero
                return (None, board.score_position(self.piece))

        if maximizing_player:
            value = -np.inf
            best_col = np.random.choice(valid_locations)

            for col in valid_locations:
                row = board.get_next_open_row(col)
                temp_board = board.board.copy()

                board.drop_piece(row, col, self.piece)
                new_score = self.minimax(board, depth - 1, alpha, beta, False)[1]
                board.board = temp_board

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
                row = board.get_next_open_row(col)
                temp_board = board.board.copy()

                board.drop_piece(row, col, self.opponent)
                new_score = self.minimax(board, depth - 1, alpha, beta, True)[1]
                board.board = temp_board

                if new_score < value:
                    value = new_score
                    best_col = col

                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cutoff

            return best_col, value

    def get_move(self, board: Board) -> int:
        """
        Get the best move for AI

        Args:
            board: Current game board

        Returns:
            Column index for the best move
        """
        print(f"\nAI is thinking (searching {self.depth} moves ahead)...")
        col, score = self.minimax(board, self.depth, -np.inf, np.inf, True)
        print(f"AI placed piece in column {col}")
        return col

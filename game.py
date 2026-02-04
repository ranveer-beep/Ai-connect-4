"""
Game Controller for Connect 4
Manages game flow and turn logic
"""

from board import Board, PLAYER, AI
from player import HumanPlayer
from ai_player import AIPlayer


class Game:
    """Main game controller"""

    def __init__(self):
        self.board = Board()
        self.player1 = HumanPlayer(PLAYER)
        self.player2 = AIPlayer(AI, depth=5)
        self.current_turn = PLAYER
        self.game_over = False

    def print_welcome(self):
        """Display welcome message"""
        print("\n" + "=" * 50)
        print("        CONNECT 4 - Player vs AI")
        print("=" * 50)
        print("\nYou are Player 1 (represented by 1)")
        print("AI is Player 2 (represented by 2)")
        print("Try to connect 4 pieces horizontally, vertically, or diagonally!")
        print("\nEnter column number (0-6) to drop your piece")
        print("=" * 50)

    def switch_turn(self):
        """Switch between players"""
        self.current_turn = AI if self.current_turn == PLAYER else PLAYER

    def play_turn(self):
        """Execute a single turn"""
        if self.current_turn == PLAYER:
            # Human player's turn
            col = self.player1.get_move(self.board)
        else:
            # AI's turn
            col = self.player2.get_move(self.board)

        # Drop the piece
        row = self.board.get_next_open_row(col)
        self.board.drop_piece(row, col, self.current_turn)

        # Check for winner
        if self.board.check_winner(self.current_turn):
            self.board.print_board()
            if self.current_turn == PLAYER:
                print("🎉 Congratulations! You won! 🎉")
            else:
                print("🤖 AI wins! Better luck next time! 🤖")
            self.game_over = True
            return

        # Check for draw
        if len(self.board.get_valid_locations()) == 0:
            self.board.print_board()
            print("Game is a draw!")
            self.game_over = True
            return

        # Continue game
        self.board.print_board()
        self.switch_turn()

    def run(self):
        """Main game loop"""
        self.print_welcome()
        self.board.print_board()

        while not self.game_over:
            self.play_turn()

        print("\nThanks for playing!")

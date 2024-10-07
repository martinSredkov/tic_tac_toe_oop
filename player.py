from abc import ABC
from random import choice

SYMBOLS = ["X", "O"]

class Player(ABC):

    marker = ""
    # randomly assign symbol for Human/AI player
    def assign_symbol(self):
        self.marker = SYMBOLS.pop(SYMBOLS.index(choice(SYMBOLS)))


class Human(Player):
    # validating user input
    def validate_input(self, player_input, min_value, max_value):
        return player_input.isdigit() and max_value >= int(player_input) >= int(min_value)
    # get move for human player
    def get_turn(self, board):
        while True:
            row = input(f"Player {self.marker}, enter row for your move:\n")
            while not self.validate_input(row, 1, len(board)):
                row = input(f"Player {self.marker}, enter valid row for your move:\n")
            row = int(row) - 1

            col = input(f"Player {self.marker}, enter column for your move:\n")
            while not self.validate_input(col, 1, len(board)):
                col = input(f"Player {self.marker}, enter valid col for your move:\n")
            col = int(col) - 1

            if board[row][col] == "-":
                return row, col, self.marker
            print("Coordinates are occupied! Enter valid coordinates.")

class AI(Player):
    # get move for AI player
    def get_turn(self,board):
        row = int(input()) - 1
        col = int(input()) - 1
        if board[row][col] == "-":
            return row, col, self.marker

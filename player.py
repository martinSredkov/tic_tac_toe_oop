from abc import ABC, abstractmethod
from random import randint

SYMBOLS = ["X", "O"]


class Player(ABC):

    def __init__(self, symbol):
        self.symbol = symbol

    @abstractmethod
    def get_turn(self, board):
        pass


class Human(Player):

    # get move for Human player

    def get_turn(self, board):
        row = input(f"Player {self.symbol}, enter row for your move:\n")
        col = input(f"Player {self.symbol}, enter column for your move:\n")
        return [row, col]



class AI(Player):

    # get move for AI player

    def get_turn(self,board):
        print("Computer's turn")
        size = len(board)
        row = str(randint(0, size - 1))
        col = str(randint(0, size - 1))
        while board[int(row)][int(col)] != "-":
            row = str(randint(0, size - 1))
            col = str(randint(0, size - 1))
        return [row, col]

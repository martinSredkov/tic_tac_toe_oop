from abc import ABC, abstractmethod
from random import randint
from utils import inp
from board import Board
from math import inf

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
        row = inp(-1,len(board),f"Player {self.symbol}, enter row for your move:\n", "Invalid row, try again:\n")
        col = inp(-1,len(board),f"Player {self.symbol}, enter column for your move:\n", "Invalid column, try again:\n")
        return [row, col]


class AI(Player):

    # get move for AI player

    def get_turn(self, board):
        size = len(board)
        row = randint(0, size - 1)
        col = randint(0, size - 1)
        while board[row][col] != "-":
            row = randint(0, size - 1)
            col = randint(0, size - 1)
        return [row, col]


class MonteCarloAI(Player):

    def __init__(self, diff_level, board_size, symbol):
        super().__init__(symbol)
        self.board_size = board_size
        self.diff_level = diff_level
        self.win_move_counter = self.get_best_moves()

    def get_best_moves(self):
        win_move_counter = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        for _ in range(self.diff_level):
            board = Board(self.board_size)
            players = [AI("X"), AI("O")]
            current = 0
            is_winner = False

            while not is_winner:
                move = players[current].get_turn(board.board)
                while not board.update(move[0], move[1], players[current].symbol):
                    move = players[current].get_turn(board.board)

                if board.win_checker(players[current].symbol):
                    is_winner = True
                    for i in range(self.board_size):
                        for j in range(self.board_size):
                            if board.board[i][j] == players[current].symbol:
                                win_move_counter[i][j] += 1
                            else:
                                win_move_counter[i][j] -= 1
                    break

                if board.is_full():
                    break

                current = 1 - current

        return win_move_counter

    def get_turn(self, board):
        max_value = -1
        row, col = -1, -1

        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == "-" and self.win_move_counter[i][j] > max_value:
                    max_value = self.win_move_counter[i][j]
                    row, col = i, j

        if row == -1 and col == -1:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == "-":
                        return [i, j]

        return [row, col]


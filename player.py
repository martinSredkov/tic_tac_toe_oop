from abc import ABC, abstractmethod
from copy import deepcopy
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


    # get best move for MonteCarloAI, play diff_level number of games and evaluate best moves

    def get_best_moves(self, board):
        move_score_board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        for _ in range(self.diff_level):
            temp_board = Board(self.board_size)
            temp_board.board = deepcopy(board)
            players = [AI("X"), AI("O")]
            current = 0
            is_winner = False


            while not is_winner:
                move = players[current].get_turn(temp_board.board)
                while not temp_board.update(move[0], move[1], players[current].symbol):
                    move = players[current].get_turn(temp_board.board)

                if temp_board.win_checker(players[current].symbol):
                    is_winner = True
                    for i in range(self.board_size):
                        for j in range(self.board_size):
                            if temp_board.board[i][j] == self.symbol:
                                move_score_board[i][j] += 1
                            else:
                                move_score_board[i][j] -= 1
                    break

                if temp_board.is_full():
                    break

                current = 1 - current

        return move_score_board

    # get move for MonteCarloAI based on the get_best_moves method, play random move if no matches are found

    def get_turn(self, board):
        max_value = -inf
        row, col = -1, -1
        best_moves = self.get_best_moves(board)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board[i][j] == "-" and best_moves[i][j] > max_value:
                    max_value = best_moves[i][j]
                    row, col = i, j

        if row == -1 and col == -1:
            for i in range(self.board_size):
                for j in range(self.board_size):
                    if board[i][j] == "-":
                        return [i, j]

        return [row, col]


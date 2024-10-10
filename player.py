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

    def save_win_coordinates(self, board, symbol):
        with open(f"winning_moves_board_size_{len(board)}.txt", "+a") as file:
            file.write(f"\n")
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y] == symbol:
                    with open(f"winning_moves_board_size_{len(board)}.txt", "+a") as file:
                        file.write(f"{x},{y}\n")

class AI(Player):

    # get move for AI player

    def get_turn(self,board):
        print("Computer's turn")
        size = len(board)
        row = randint(0, size - 1)
        col = randint(0, size - 1)
        while board[row][col] != "-":
            row = randint(0, size - 1)
            col = randint(0, size - 1)
        return [row, col]

    def save_win_coordinates(self, board, symbol):
        with open(f"winning_moves_board_size_{len(board)}.txt", "+a") as file:
            file.write(f"\n")
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y] == symbol:
                    with open(f"winning_moves_board_size_{len(board)}.txt", "+a") as file:
                        file.write(f"{x},{y}\n")

class MonteCarloAI(Player):

    def get_turn(self, board):
        line = 0
        with open(f"winning_moves_board_size_{len(board)}.txt", "+r") as file:
            list_of_moves = file.readlines()
            size = len(list_of_moves)
        while line < size:
            move = [list_of_moves[line]].pop()
            size -= 1
            move = move.strip()
            if move == "":
                line += 1
                continue
            row, col = move.split(",")
            row = int(row)
            col = int(col)
            if board[row][col] != "-":
                line += 1
                continue
            return [row, col]

    def save_win_coordinates(self, board, symbol):
        with open(f"winning_moves_board_size_{len(board)}.txt", "+a") as file:
            file.write(f"\n")
        for x in range(len(board)):
            for y in range(len(board)):
                if board[x][y] == symbol:
                    with open(f"winning_moves_board_size_{len(board)}.txt", "+a") as file:
                        file.write(f"{x},{y}\n")

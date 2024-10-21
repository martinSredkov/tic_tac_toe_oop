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
        row = inp(0,board.size,f"Player {self.symbol}, enter row for your move:\n", "Invalid row, try again:\n")
        col = inp(0,board.size,f"Player {self.symbol}, enter column for your move:\n", "Invalid column, try again:\n")
        return [row, col]


class AI(Player):

    # get move for AI player

    def get_turn(self, board):
        row = randint(0, len(board) - 1)
        col = randint(0, len(board) - 1)
        while board[row][col] != "-":
            row = randint(0, len(board) - 1)
            col = randint(0, len(board) - 1)
        return [row, col]


class MonteCarloAI(Player):

    def __init__(self, diff_level, board_size, symbol):
        super().__init__(symbol)
        self.board_size = board_size
        self.diff_level = diff_level


    # get best move for MonteCarloAI, play diff_level number of games and evaluate best moves

    def get_best_moves(self, board, ):
        other = [x.symbol for x in board.players if x.symbol is not self.symbol][0]
        move_score_board = [[0 for _ in range(board.size)] for _ in range(board.size)]
        for _ in range(self.diff_level):
            temp_board = Board(board.size)
            temp_board.board = deepcopy(board.board)
            temp_board.set_players(board.players)
            players = [AI(self.symbol), AI(other)]
            current=0
            is_winner = False

            while not is_winner:
                move = players[current].get_turn(temp_board.board)
                while not temp_board.update(move[0], move[1], players[current].symbol):
                    move = players[current].get_turn(temp_board.board)

                if temp_board.win_checker(players[current].symbol):
                    is_winner = True
                    mul_mod = 1 if players[current].symbol == self.symbol else -1
                    for i in range(self.board_size):
                        for j in range(self.board_size):
                            if temp_board.board[i][j] == self.symbol :
                                move_score_board[i][j] += 1*mul_mod
                            elif temp_board.board[i][j] == other:
                                move_score_board[i][j] -= 1*mul_mod
                    break

                if temp_board.is_full():
                    break

                current = 1 - current

        return move_score_board

    # get move for MonteCarloAI based on the get_best_moves method, play random move if no matches are found

    def get_turn(self, board):
        max_value = -inf
        best_moves = self.get_best_moves(board)
        for i in range(self.board_size):
            for j in range(self.board_size):
                if board.board[i][j] == "-" and best_moves[i][j] > max_value:
                    max_value = best_moves[i][j]
                    row, col = i, j
        return [row, col]


class MinMax(Player):

    def get_possible_moves(self, board):
        possible_moves = []
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] == "-":
                    possible_moves.append([i, j])
        return possible_moves


    def get_best_move(self, board, moves, turn):
        if board.is_full():
            return 0, None
        if board.win_checker(self.symbol):
            return 1, None
        elif board.win_checker(SYMBOLS[SYMBOLS.index(self.symbol) - 1]):
            return - 1, None

        best_move = None
        if turn:
            best_score = -inf
        else:
            best_score = inf

        for move in moves:
            if turn:
                board.board[move[0]][move[1]] = self.symbol
            else:
                board.board[move[0]][move[1]] = SYMBOLS[SYMBOLS.index(self.symbol) - 1]
            score, _ = self.get_best_move(board, self.get_possible_moves(board), not turn)
            board.board[move[0]][move[1]] = "-"

            if turn:
                if score >= best_score:
                    best_score = score
                    best_move = move
            else:
                if score <= best_score:
                    best_score = score
                    best_move = move

        return best_score, best_move

    def get_turn(self, board):
        _, best_move = self.get_best_move(board, self.get_possible_moves(board), True)
        return best_move

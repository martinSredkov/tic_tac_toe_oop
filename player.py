from abc import ABC, abstractmethod
from copy import deepcopy
from random import randint
from utils import inp
from board import Board
from math import inf
import operator

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

    def __init__(self, symbol):
        super().__init__(symbol)
        self.memo = {}
        self.symmetry_hashes = set()

    # get all possible moves in board's current state
    def get_possible_moves(self, board):
        possible_moves = []
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] == "-":
                    possible_moves.append([i, j])
        return possible_moves

    # flatten board
    def hash_func(self, board):
        return ''.join(''.join(row) for row in board)

    # rotating the board 90 degrees clockwise
    def rotate_board(self, board):
        return [list(reversed(col)) for col in zip(*board)]

    # mirror board's current state
    def mirror_board(self, board_matrix):
        return [row[::-1] for row in board_matrix]

    # generate all possible symmetrical states for current board's state
    def generate_symmetrical_states(self, board):
        sym_hashes = set()
        current_board = board.board

        sym_hashes.add(self.hash_func(current_board))
        sym_hashes.add(self.hash_func(self.mirror_board(current_board)))

        for _ in range(3):
            current_board = self.rotate_board(current_board)
            sym_hashes.add(self.hash_func(current_board))

        return sym_hashes

    # check current board's state for symmetries
    def is_symmetric(self, board):
        return any(hash_state in self.symmetry_hashes for hash_state in self.generate_symmetrical_states(board))

    # get best move by ranking all possible moves recursively and taking the best score
    def get_best_move(self, board, moves, turn, alpha=-inf, beta=inf):
        other = SYMBOLS[SYMBOLS.index(self.symbol) - 1]
        board_hash = self.hash_func(board.board)

        if board_hash in self.memo:
            return self.memo[board_hash]

        if self.is_symmetric(board):
            if board_hash in self.generate_symmetrical_states(board):
                return board_hash

        if board.is_full():
            return 0, None
        if board.win_checker(self.symbol):
            return 1, None
        elif board.win_checker(other):
            return -1, None

        best_move = None
        best_score = -inf if turn else inf

        for move in moves:
            board.board[move[0]][move[1]] = self.symbol if turn else other
            score, _ = self.get_best_move(board, self.get_possible_moves(board), not turn, alpha, beta)
            board.board[move[0]][move[1]] = "-"

            if turn:
                if score > best_score:
                    best_score, best_move = score, move
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            else:
                if score < best_score:
                    best_score, best_move = score, move
                beta = min(beta, best_score)
                if beta <= alpha:
                    break

        self.memo[board_hash] = (best_score, best_move)
        return best_score, best_move

    # get turn method that sets the first move to the middle of the board
    def get_turn(self, board):
        moves = self.get_possible_moves(board)
        if len(moves) == board.size * board.size:
            return [board.size // 2, board.size // 2]
        best_score, best_move = self.get_best_move(board, moves, True)
        return best_move


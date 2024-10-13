from random import randint
from board import Board
from player import AI, Human, MonteCarloAI
from utils import inp
from math import inf


class Game:

    # assigning player types based on number of AI players

    def assign_type(self, ai_count, board_size):
        if ai_count == 0:
            player_1 = Human("X")
            player_2 = Human("O")
        else:
            ai_difficulty = inp(0, inf,"Choose computer player difficulty by typing a number:\n", "Type a positive number:\n")
            if ai_count > 1:
                player_1 = MonteCarloAI(ai_difficulty, board_size, "X")
                player_2 = MonteCarloAI(ai_difficulty, board_size, "O")
            else:
                player_1 = MonteCarloAI(ai_difficulty, board_size, "X")
                player_2 = Human("O")
        return player_1, player_2

    # starting the game, user inputs for board size and type of players

    def start(self):
        board = Board(inp(2,inf, "Enter board size:\n", "Enter board size, >= 3:\n"))
        ai_players = inp(-1, 3,"Enter number of computer players(0-2):\n","Enter valid number of computer players(0-2):\n")
        players = self.assign_type(ai_players, len(board.board))
        board.display()
        current = randint(0, 1)

        # getting Human/AI input for move

        while True:
            move = players[current].get_turn(board.board)
            while not board.update(move[0], move[1], players[current].symbol):
                move = players[current].get_turn(board.board)
            board.display()
            if board.win_checker(players[current].symbol):
                print(f"Player {players[current].symbol} is winner!")
                board.display()
                exit(0)
            elif board.is_full():
                print("Draw!")
                board.display()
                exit(0)

            # switching player
            current += 1
            if current > 1:
                current = 0

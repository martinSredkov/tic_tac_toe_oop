from random import randint
from board import Board
from player import AI, Human, MonteCarloAI

MAX_PLAYERS = 2

class Game:

    # validating user input

    def validate_input(self, player_input, min_value):
        return player_input.isdigit() and int(player_input) >= int(min_value)

    # assigning player types based on number of AI players

    def assign_type(self, ai_count):
        difficulties = [AI, MonteCarloAI]
        if int(ai_count) == 0:
            player_1 = Human("X")
            player_2 = Human("O")
        else:
            ai_difficulty = input("Choose computer player difficulty by typing a number:\n1.Easy\n2.Medium\n")
            while not ai_difficulty.isdigit() or 1 < int(ai_difficulty) > 2:
                ai_difficulty = input("Type 1 for easy or 2 for medium difficulty:\n")
            ai_difficulty = int(ai_difficulty)

            if int(ai_count) > 1:
                player_1 = difficulties[ai_difficulty - 1]("X")
                player_2 = difficulties[ai_difficulty - 1]("O")
            else:
                player_1 = difficulties[ai_difficulty - 1]("X")
                player_2 = Human("O")
        return player_1, player_2

    # starting the game user inputs for board size and type of players

    def start(self):
        board = Board(input("Enter board size:\n"))
        ai_players = input("Enter number of computer players(0-2):\n")
        while not self.validate_input(ai_players, 0) or int(ai_players) > MAX_PLAYERS:
            ai_players = input("Enter valid number of computer players(0-2):\n")
        players = self.assign_type(ai_players)
        board.display()
        current = randint(0, 1)

        # getting User/AI input for move

        while True:
            move = players[current].get_turn(board.board)
            while not board.update(move[0], move[1], players[current].symbol):
                move = players[current].get_turn(board.board)
            board.display()
            result = [
                      board.horizontal_check(board.board, players[current].symbol),
                      board.vertical_check(board.board, players[current].symbol),
                      board.left_diagonal_check(board.board, players[current].symbol),
                      board.right_diagonal_check(board.board, players[current].symbol)
            ]
            if any(result):
                print(f"Player {players[current].symbol} is winner!")
                players[current].save_win_coordinates(board.board, players[current].symbol)
                exit(0)
            elif board.is_full():
                print("Draw!")
                exit(0)

            # switching player

            current += 1
            if current > 1:
                current = 0

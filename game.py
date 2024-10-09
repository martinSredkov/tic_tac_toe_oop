from random import randint
from board import Board
from player import AI, Human

MAX_PLAYERS = 2

class Game:

    # validating user input

    def validate_input(self, player_input, min_value):
        return player_input.isdigit() and int(player_input) >= int(min_value)

    #TODO Optimize

    # checks for horizontal win

    def horizontal_check(self, board, symbol):
        board_size = len(board)
        for line in board:
            for el in line:
                if el != symbol:
                    board_size = len(board)
                    break
                board_size -= 1
                if board_size == 0:
                    return True

    # checks for vertical win

    def vertical_check(self, board, symbol):
        board_size = len(board)
        win = board_size
        for k in range(board_size):
            for j in range(board_size):
                if board[j][k] != symbol:
                    win = board_size
                    break
                win -= 1
                if win == 0:
                    return True

    # checks for left diagonal win

    def left_diagonal_check(self, board, symbol):
        board_size = len(board)
        win = board_size
        for l in range(board_size):
            if board[l][l] != symbol:
                return False
            win -= 1
            if win == 0:
                return True

    # checks for right diagonal win

    def right_diagonal_check(self, board, symbol):
        board_size = len(board)
        win = board_size
        for m in range(board_size, 0, - 1):
            if board[board_size - m][m - 1] != symbol:
                return  False
            win -= 1
            if win == 0:
                return True

    # assigning player types based on number of AI players

    def assign_type(self, ai_count):
        if int(ai_count) == 0:
            player_1 = Human("X")
            player_2 = Human("O")
        elif int(ai_count) > 1:             #TODO input for AI difficulty
            player_1 = AI("X")
            player_2 = AI("O")
        else:
            player_1 = AI("X")
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
                      self.horizontal_check(board.board, players[current].symbol),
                      self.vertical_check(board.board, players[current].symbol),
                      self.left_diagonal_check(board.board, players[current].symbol),
                      self.right_diagonal_check(board.board, players[current].symbol)
            ]
            if any(result):
                print(f"Player {players[current].symbol} is winner!")
                exit(0)
            elif board.is_full():
                print("Draw!")
                exit(0)

            # switching player

            current += 1
            if current > 1:
                current = 0

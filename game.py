from board import Board
from player import AI, Human

MAX_PLAYERS = 2

class Game:
    # validating user input
    def validate_input(self, player_input, min_value):
        return player_input.isdigit() and int(player_input) >= int(min_value)
    # universal win condition check
    def win_check(self, lst):
        if len(set(lst)) == 1 and "-" not in lst:
            return True
    # adds elements of rows, columns and diagonals to separate lists and passes them to win_check function
    def is_player_winner(self, board):
        result = []
        board_size = len(board)
        # checks if winning conditions are met in rows
        for line in board:
            if self.win_check(line):
                return True
        # checks if winning conditions are met in columns
        for k in range(board_size):
            for j in range(board_size):
                result.append(board[j][k])
            if self.win_check(result):
                return True
            result = []
        if self.win_check(result):
            return True
        # checks if winning conditions are met in left to right diagonal
        for l in range(board_size):
            result.append(board[l][l])
        if self.win_check(result):
            return True
        result = []
        # checks if winning conditions are met in right to left diagonal
        for m in range(board_size, 0, - 1):
            result.append(board[board_size - m][m - 1])
        if self.win_check(result):
            return True
    # assigning player types based on number of AI players
    def assign_type(self, ai_count):
        player_types = [Human, AI]
        if int(ai_count) > 1:
            player_1 = player_types[1]()
            player_2 = player_types[1]()
        elif int(ai_count) == 0:
            player_1 = player_types[0]()
            player_2 = player_types[0]()
        else:
            player_1 = player_types[1]()
            player_2 = player_types[0]()
        player_1.assign_symbol()
        player_2.assign_symbol()
        return player_1, player_2
    # starting the game user inputs for board size and type of players
    def start(self):
        board = Board(input("Enter board size:\n"))
        ai_players = input("Enter number of computer players(0-2):\n")
        while not self.validate_input(ai_players, 0) or int(ai_players) > MAX_PLAYERS:
            ai_players = input("Enter valid number of computer players(0-2):\n")
        players = self.assign_type(ai_players)
        board.display()
        current = 0
        # getting User/AI input for move
        while True:
            move = players[current].get_turn(board.board)
            board.update(*move)
            board.display()
            if self.is_player_winner(board.board):
                print(f"Player {players[current].marker} is winner!")
                exit(0)
            elif board.is_full():
                print("Draw!")
                exit(0)
            # switching player
            current += 1
            if current > 1:
                current = 0

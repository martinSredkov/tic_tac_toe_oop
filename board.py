from prettytable import PrettyTable

MIN_BOARD_SIZE = 3

table = PrettyTable()

class Board:

    # initialize board with user given size

    def __init__(self, size):
        while not self.validate_input(size, MIN_BOARD_SIZE):
            size = input("Enter board size, >= 3:\n")
        self.size = int(size)
        self.board = []
        for i in range(self.size):
            self.board.append([])
            [self.board[i].append("-") for _ in range(self.size)]

    # validate input

    def validate_input(self, player_input, min_value):
        return player_input.isdigit() and int(player_input) >= int(min_value)

    # draw condition check (are there any empty spaces left)

    def is_full(self):
        for line in self.board:
            for element in line:
                if element == "-":
                    return False
        return True

    # displaying the board

    def display(self):
        for line in self.board:
            table.add_row(line)
        print(table.get_string(border=True, header=False, align="c", hrules=1))
        table.clear()

    # updating the board with given coordinates and symbol

    def update(self, row, col, marker):
        if self.validate_input(row, 0) and self.validate_input(col, 0):
            if int(row) < len(self.board) and int(col) < len(self.board):
                if self.board[int(row)][int(col)] == "-":
                    self.board[int(row)][int(col)] = marker
                    return self.board
                print("Coordinates are occupied.")
        print("Invalid coordinates.")
        return False

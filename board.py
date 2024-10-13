from prettytable import PrettyTable


table = PrettyTable()

class Board:

    # initialize board with user given size

    def __init__(self, size):
        self.size = int(size)
        self.board = [["-" for _ in range(self.size)] for _ in range(self.size)]


    # draw condition check (are there any empty spaces left)

    def is_full(self):
        for line in self.board:
            for element in line:
                if element == "-":
                    return False
        return True

    # checks for horizontal win

    def horizontal_check(self, symbol):
        win = len(self.board)
        for line in self.board:
            for el in line:
                if el != symbol:
                    win = len(self.board)
                    break
                win -= 1
                if win == 0:
                    return True

    # checks for vertical win

    def vertical_check(self, symbol):
        win = self.size
        for k in range(self.size):
            for j in range(self.size):
                if self.board[j][k] != symbol:
                    win = self.size
                    break
                win -= 1
                if win == 0:
                    return True

    # checks for left diagonal win

    def left_diagonal_check(self, symbol):
        win = self.size
        for l in range(self.size):
            if self.board[l][l] != symbol:
                return False
            win -= 1
            if win == 0:
                return True

    # checks for right diagonal win

    def right_diagonal_check(self, symbol):
        win = self.size
        for m in range(self.size, 0, - 1):
            if self.board[self.size - m][m - 1] != symbol:
                return  False
            win -= 1
            if win == 0:
                return True

    # checks the board with winning conditions

    def win_checker(self, symbol):

        win_checks = [
            self.horizontal_check,
            self.vertical_check,
            self.left_diagonal_check,
            self.right_diagonal_check
        ]
        for check in win_checks:
            if check(symbol):
                return True

    # displaying the board

    def display(self):
        table.clear()
        for line in self.board:
            table.add_row(line)
        print(table.get_string(border=True, header=False, align="c", hrules=1))
        return table.get_string(border=True, header=False, align="c", hrules=1)


    # updating the board with given coordinates and symbol

    def update(self, row, col, symbol):
        if self.board[int(row)][int(col)] == "-":
            self.board[int(row)][int(col)] = symbol
            return self.board
        print("Coordinates are occupied.")
        return False


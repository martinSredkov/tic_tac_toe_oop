from prettytable import PrettyTable

table = PrettyTable()

class Board:
    # initialize board with user given size
    def __init__(self, size):
        self.size = int(size)
        self.board = []
        for i in range(self.size):
            self.board.append([])
            [self.board[i].append("-") for _ in range(self.size)]
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
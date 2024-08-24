import random
import time


class Board:
    def __init__(self, grid):
        self.grid = grid
        self.editable = [[grid[row][col] == 0 for col in range(9)] for row in range(9)]
        self.is_cleared = False

    def _update(self):
        self.editable = [[self.grid[row][col] == 0 for col in range(9)] for row in range(9)]

    def clear(self, only_editable=False):
        if only_editable:
            for row in range(9):
                for col in range(9):
                    if self.editable[row][col]:
                        self.grid[row][col] = 0
        else:
            self.grid = [[0] * 9 for _ in range(9)]
            self.editable = [[True] * 9 for _ in range(9)]
            self.is_cleared = True

    def is_valid(self, row, col, num):
        for i in range(9):
            if (self.grid[row][i] == num and i != col) or (self.grid[i][col] == num and i != row):
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.grid[start_row + i][start_col + j] == num and (start_row + i, start_col + j) != (row, col):
                    return False
        return True

    def find_empty(self):
        for row in range(9):
            for col in range(9):
                if self.grid[row][col] == 0:
                    return [row, col]
        return None

    def solve(self, random_selection=False):
        empty = self.find_empty()
        if empty is None:
            return True
        row, col = empty

        numbers = list(range(1, 10))
        if random_selection:  # Use random selection when you want to create new puzzles
            random.shuffle(numbers)

        for num in numbers:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                if self.solve(random_selection):
                    return True
                self.grid[row][col] = 0
        return False

    def solve_with_visualization(self, draw_func, timer):
        empty = self.find_empty()
        if empty is None:
            return True

        row, col = empty
        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                draw_func(self, valid_cell=[row, col])

                # Adjust sleep time based on solving elapsed time
                solving_elapsed_time = timer.solving_elapsed_time
                sleep_time = max(0.1 - solving_elapsed_time * 0.002, 0.0001)  # Decrease sleep time over time
                time.sleep(sleep_time)

                if self.solve_with_visualization(draw_func, timer):
                    return True

                self.grid[row][col] = 0
                draw_func(self, invalid_cell=[row, col])
                time.sleep(sleep_time)

        return False

    @classmethod
    def generate(cls, num_holes=45):
        grid = [[0] * 9 for _ in range(9)]
        board = cls(grid)
        board.solve(random_selection=True)

        # Remove numbers to create the puzzle
        count = num_holes
        while count > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while board.grid[row][col] == 0:
                row, col = random.randint(0, 8), random.randint(0, 8)
            board.grid[row][col] = 0
            count -= 1
        board._update()
        return board

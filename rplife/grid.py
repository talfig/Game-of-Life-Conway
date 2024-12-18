# rplife/grid.py

import collections


class LifeGrid:
    def __init__(self, pattern, grid_size=20):
        self.pattern = pattern
        self.end_row = grid_size
        self.end_col = grid_size

    def evolve(self):
        neighbors = (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),         (0, 1),
            (1, -1), (1, 0), (1, 1),
        )

        num_neighbors = collections.defaultdict(int)
        for row, col in self.pattern:
            for drow, dcol in neighbors:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row <= self.end_row and 0 <= new_col <= self.end_col:
                    num_neighbors[(new_row, new_col)] += 1

        stay_alive = {
                         cell for cell, num in num_neighbors.items() if num in {2, 3}
                     } & self.pattern
        come_alive = {
                         cell for cell, num in num_neighbors.items() if num == 3
                     } - self.pattern

        self.pattern = stay_alive | come_alive

    def get_size(self):
        return len(self.pattern)

# rplife/grid.py

import collections


class LifeGrid:
    """
    A class representing a grid for Conway's Game of Life. It holds the current pattern of live cells
    and provides functionality for evolving the grid according to the rules of the game.
    """

    def __init__(self, pattern, grid_size=20):
        """
        Initializes the LifeGrid with the given initial pattern and grid size.

        Args:
            pattern (set): A set of tuples representing the initial live cell coordinates.
            grid_size (int, optional): The size of the grid. The default is 20, creating a 20x20 grid.
        """
        self.pattern = pattern
        self.end_row = grid_size
        self.end_col = grid_size

    def evolve(self):
        """
        Evolves the grid to the next generation based on the Game of Life rules:
        - A live cell with two or three live neighbors stays alive.
        - A dead cell with exactly three live neighbors comes to life.
        - All other cells either stay dead or die.

        Updates the pattern attribute with the new set of live cells for the next generation.
        """
        neighbors = (
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1), (1, 0), (1, 1),
        )

        num_neighbors = collections.defaultdict(int)

        # Count the number of neighbors for each live cell
        for row, col in self.pattern:
            for drow, dcol in neighbors:
                new_row, new_col = row + drow, col + dcol
                if 0 <= new_row <= self.end_row and 0 <= new_col <= self.end_col:
                    num_neighbors[(new_row, new_col)] += 1

        # Determine which cells stay alive and which cells come to life
        stay_alive = {
                         cell for cell, num in num_neighbors.items() if num in {2, 3}
                     } & self.pattern
        come_alive = {
                         cell for cell, num in num_neighbors.items() if num == 3
                     } - self.pattern

        # Update the pattern with cells that stay alive or come alive
        self.pattern = stay_alive | come_alive

    def get_size(self):
        """
        Returns the number of live cells in the current pattern.

        Returns:
            int: The number of live cells in the pattern.
        """
        return len(self.pattern)

# rplife/simulation.py

import copy
from rplife.grid import LifeGrid


class Simulation:
    """
    A class to simulate the evolution of a LifeGrid for a given number of generations or until stabilization.
    """

    def __init__(self, life: LifeGrid, gen_limit=400):
        """
        Initializes the simulation with the given LifeGrid and generation limit.

        Args:
            life (LifeGrid): An instance of the LifeGrid class representing the initial state of the grid.
            gen_limit (int, optional): The maximum number of generations to simulate. Default is 400.
        """
        self.life = copy.deepcopy(life)

        self.gen = 0
        self.gen_limit = gen_limit

        self.size = self.life.get_size()
        self.max_size = self.size
        self.max_size_gen = self.gen
        self.gen_history = []

    def simulate(self):
        """
        Runs the simulation for the specified number of generations or until stabilization occurs.
        Each generation, the pattern evolves, and the size is updated. The history of patterns is recorded.

        The simulation stops if the maximum number of generations is reached or if the pattern stabilizes.
        """
        while self.gen <= self.gen_limit and not self.stabilized():
            self.gen += 1

            # Record the current pattern for stabilization check
            self.gen_history.append(copy.deepcopy(self.life.pattern))
            self.life.evolve()  # Evolve the pattern for the next generation
            self.update_size()  # Update the current size of the pattern

    def stabilized(self):
        """
        Checks if the pattern has stabilized, i.e., if it has appeared before in the simulation history.

        Returns:
            bool: True if the pattern has stabilized, otherwise False.
        """
        return self.life.pattern in self.gen_history

    def update_size(self):
        """
        Updates the current size of the pattern and tracks the maximum size encountered during the simulation.
        If the current size exceeds the maximum size, it updates the max_size and the generation at which it occurred.
        """
        self.size = self.life.get_size()
        if self.size > self.max_size:
            self.max_size = self.size
            self.max_size_gen = self.gen

    def get_max_size(self):
        """
        Returns the maximum size of the pattern encountered during the simulation.

        Returns:
            int: The maximum size of the pattern.
        """
        return self.max_size

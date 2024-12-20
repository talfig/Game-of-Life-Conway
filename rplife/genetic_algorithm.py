# rplife/genetic_algorithm.py

import random
from copy import deepcopy

from rplife.grid import LifeGrid
from rplife.simulation import Simulation
from rplife.pattern import save_to_toml


class GeneticAlgorithm:
    """
    Class for implementing a Genetic Algorithm to find a "Methuselah" pattern
    in Conway's Game of Life.

    This algorithm evolves a population of LifeGrids (chromosomes) through
    selection, crossover, and mutation operations. It attempts to find a
    "Methuselah" (a pattern that lives for a long time) based on the fitness
    function that measures the maximum size achieved by a LifeGrid during its evolution.
    """

    def __init__(self, pop_size=50, grid_size=20, min_cells=5, max_cells=10, gen_limit=200,
                 crossover_prob=0.8, mutation_prob=0.8, mutation_count=3, threshold_fit=100):
        """
        Initializes the Genetic Algorithm.

        Args:
            pop_size (int): The size of the population.
            grid_size (int): The grid size for LifeGrid.
            min_cells (int): Minimum number of alive cells in a chromosome.
            max_cells (int): Maximum number of alive cells in a chromosome.
            gen_limit (int): Generation limit for the simulation of each LifeGrid.
            crossover_prob (float): Probability of performing crossover.
            mutation_prob (float): Probability of performing mutation.
            threshold_fit (int): Target fitness value to find a "Methuselah".
        """
        self.pop_size = pop_size
        self.grid_size = grid_size
        self.min_cells = min_cells
        self.max_cells = max_cells
        self.gen_limit = gen_limit
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.mutation_count = mutation_count
        self.threshold_fit = threshold_fit  # Threshold fitness for Methuselah
        self.population = []
        self.pop_fit = 0  # Total fitness of the population

    def find_methuselah(self):
        """
        Runs the Genetic Algorithm to find a LifeGrid (chromosome) whose fitness exceeds the threshold_fit.
        Stops if the generation limit is reached.

        Returns:
            tuple: (LifeGrid, fitness) of the Methuselah pattern if found, or (None, None) if not found.
        """
        # Step 1: Initialize population
        self.init_population()
        generation = 0

        while generation < self.gen_limit:  # Stop when generation limit is reached
            # Variable to track the best fitness in the current generation
            best_fitness = 0

            # Step 2: Check for Methuselah in the current population
            for individual in self.population:
                fitness = self.get_fitness(individual)

                # Update the best fitness if the current fitness is higher
                if fitness > best_fitness:
                    best_fitness = fitness

                # Check if the threshold fitness (Methuselah) is reached
                if fitness >= self.threshold_fit:
                    print(f"Found Methuselah in generation {generation} with fitness: {fitness}")
                    return individual, fitness

            # Print the best fitness every 10 generations
            if generation % 10 == 0:
                print(f"Generation {generation}: Best fitness so far: {best_fitness}")

            # Step 3: No Methuselah found, create the next generation
            self.next_generation()
            generation += 1

        # If no Methuselah was found within the generation limit
        print(f"Reached generation limit ({self.gen_limit}). No Methuselah found.")
        return None, None

    def generate_chromosome(self):
        """
        Generates a LifeGrid object with a random initial configuration.

        Returns:
            LifeGrid: A LifeGrid object with a random pattern.
        """
        num_cells = random.randint(self.min_cells, self.max_cells)  # Random number of cells
        random_pattern = set()

        while len(random_pattern) < num_cells:
            row = random.randint(self.grid_size // 4, 3 * self.grid_size // 4 - 1)
            col = random.randint(self.grid_size // 4, 3 * self.grid_size // 4 - 1)
            random_pattern.add((row, col))  # Add unique (row, col) coordinates

        return LifeGrid(random_pattern, self.grid_size)

    @staticmethod
    def get_fitness(chromosome: LifeGrid):
        """
        Calculates the fitness of a chromosome based on the max size from simulation.

        Args:
            chromosome (LifeGrid): A LifeGrid object representing a chromosome.

        Returns:
            float: Fitness value for the chromosome based on max size after simulation.
        """
        sim = Simulation(chromosome)  # Simulate the chromosome
        sim.simulate()  # Run the simulation
        max_size = sim.get_max_size()  # Get the max size reached during the simulation
        return max_size

    def init_population(self):
        """
        Initializes the population of LifeGrid objects.

        Returns:
            list: A list of LifeGrid objects (the population).
        """
        self.population = []  # Reset population
        self.pop_fit = 0  # Reset total fitness

        for _ in range(self.pop_size):
            chromosome = self.generate_chromosome()
            self.population.append(chromosome)
            self.pop_fit += self.get_fitness(chromosome)  # Fitness based on max size

    def selection(self):
        """
        Selects exactly two parents based on the roulette wheel selection method.
        The probability of selecting a chromosome is proportional to its fitness.

        Returns:
            list: A list containing two selected parent chromosomes.
        """
        # Step 1: Calculate the probability for each chromosome
        probabilities = [self.get_fitness(chromosome) / self.pop_fit for chromosome in self.population]

        selected = []

        # Step 2: Select two parents based on their probabilities
        for _ in range(2):  # We always select exactly two parents
            random_choice = random.random()
            cumulative_prob = 0
            for i, prob in enumerate(probabilities):
                cumulative_prob += prob
                if random_choice <= cumulative_prob:
                    selected.append(self.population[i])
                    break

        return selected

    def crossover(self, parent1: LifeGrid, parent2: LifeGrid):
        """
        Perform position-based crossover to create offspring.

        Args:
            parent1 (LifeGrid): The first parent individual.
            parent2 (LifeGrid): The second parent individual.

        Returns:
            tuple: Two LifeGrid objects representing the offspring.
        """
        if random.random() > self.crossover_prob:
            return parent1, parent2

        # Generate offspring positions
        child1_positions = self._crossover_positions(parent1.pattern, parent2.pattern)
        child2_positions = self._crossover_positions(parent2.pattern, parent1.pattern)

        # Create offspring as LifeGrid objects
        child1 = LifeGrid(child1_positions, self.grid_size)
        child2 = LifeGrid(child2_positions, self.grid_size)

        return child1, child2

    def _crossover_positions(self, primary_pattern: set, secondary_pattern: set):
        """
        Generate a set of positions for an offspring using a two-step sampling process.

        Args:
            primary_pattern (set): The pattern from the primary parent.
            secondary_pattern (set): The pattern from the secondary parent.

        Returns:
            set: A set of positions for the offspring.
        """
        # Sample half of the max cells from the primary pattern
        max_primary_sample = min(len(primary_pattern), self.max_cells // 2)
        offspring_positions = set(random.sample(list(primary_pattern), max_primary_sample))

        # Fill remaining positions from the secondary pattern
        max_secondary_sample = min(len(secondary_pattern - offspring_positions),
                                   self.max_cells - len(offspring_positions))
        offspring_positions.update(random.sample(list(secondary_pattern - offspring_positions), max_secondary_sample))

        return offspring_positions

    def mutation(self, individual):
        """
        Apply mutation to an individual by adding or removing cells in its pattern.

        Args:
            individual (LifeGrid): The individual to mutate.

        Returns:
            LifeGrid: The mutated individual.
        """
        for _ in range(self.mutation_count):
            if random.random() < self.mutation_prob:
                # Create a copy of the individual's pattern
                new_pattern = set(individual.pattern)

                # Decide whether to add or remove a cell
                if random.random() < 0.5 and new_pattern:  # Remove an existing cell
                    new_pattern.remove(random.choice(list(new_pattern)))
                else:  # Add a new cell within grid bounds
                    new_cell = (random.randint(self.grid_size // 4, 3 * self.grid_size // 4 - 1), random.randint(self.grid_size // 4, 3 * self.grid_size // 4 - 1))
                    if len(new_pattern) < self.max_cells:
                        new_pattern.add(new_cell)

                # Ensure the pattern respects the max_cells constraint
                if len(new_pattern) > self.max_cells:
                    new_pattern = set(list(new_pattern)[:self.max_cells])

                # Update the individual with the new mutated pattern
                individual = LifeGrid(new_pattern, self.grid_size)

        return individual

    def next_generation(self):
        """
        Generate the next generation of the population using elitism, crossover, and mutation.

        Steps:
            1. Sort the population by fitness.
            2. Retain the top 10% of individuals as the elite group.
            3. Split the elite group into top and bottom halves.
            4. Fill the next generation by combining crossover and mutation.

        Updates:
            self.population: Replaces the current population with the new generation.
        """
        # Sort the population by fitness in descending order
        sorted_population = sorted(self.population, key=lambda ind: self.get_fitness(ind), reverse=True)

        # Determine the size of the elite group (top 10%)
        elite_size = max(1, int(0.1 * len(self.population)))  # Ensure at least one elite individual
        elite_group = sorted_population[:elite_size]

        # Split the elite group into the top 50% and bottom 50%
        top_elite_size = elite_size // 2
        top_elite = elite_group[:top_elite_size]
        bottom_elite = elite_group[top_elite_size:]

        # Initialize the next generation with the top elite individuals
        next_gen = deepcopy(top_elite)

        # Perform crossover and mutation to fill the rest with the population
        non_elite_population = sorted_population[elite_size:]
        while len(next_gen) < len(self.population):
            # Randomly select parents for crossover
            parent1 = random.choice(bottom_elite)
            parent2 = random.choice(non_elite_population)

            # Generate offspring through crossover
            child1, child2 = self.crossover(parent1, parent2)

            # Apply mutation to the offspring
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            # Add the offspring to the next generation, maintaining population size
            next_gen.append(child1)
            if len(next_gen) < len(self.population):
                next_gen.append(child2)

        # Update the population with the new generation
        self.population = next_gen


if __name__ == "__main__":
    # Initialize the Genetic Algorithm
    ga = GeneticAlgorithm(pop_size=100, grid_size=20, gen_limit=500, threshold_fit=100)

    # Find Methuselah
    methuselah = ga.find_methuselah()

    if methuselah[0]:
        print(f"Found Methuselah pattern with fitness {methuselah[1]}!")

        # Save Methuselah pattern to a TOML file
        save_to_toml(methuselah[0].pattern, methuselah[1])
    else:
        print("No Methuselah pattern found within generation limit.")

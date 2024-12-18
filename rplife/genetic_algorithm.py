# rplife/genetic_algorithm.py

import random
from copy import deepcopy

from rplife.grid import LifeGrid
from rplife.simulation import Simulation
from rplife.pattern import save_to_toml


class GeneticAlgorithm:
    def __init__(self, pop_size=100, grid_size=20, min_cells=5, max_cells=10, gen_limit=200,
                 crossover_prob=0.8, mutation_prob=0.8, threshold_fit=100):
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
            row = random.randint(0, self.grid_size)
            col = random.randint(0, self.grid_size)
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
        # Check if crossover should occur based on probability
        if random.random() > self.crossover_prob:
            return parent1, parent2

        # Perform uniform crossover
        child1_pattern = set()
        child2_pattern = set()
        all_positions = parent1.pattern | parent2.pattern  # Combine all positions from both parents

        for position in all_positions:
            if random.random() < 0.5:  # Randomly assign positions to child1 or child2
                if len(child1_pattern) < self.max_cells:
                    child1_pattern.add(position)
            else:
                if len(child2_pattern) < self.max_cells:
                    child2_pattern.add(position)

        # Create new LifeGrid objects for the children
        child1 = LifeGrid(child1_pattern, self.grid_size)
        child2 = LifeGrid(child2_pattern, self.grid_size)

        return child1, child2

    def mutation(self, individual: LifeGrid):
        # Perform mutation only if random < mutation_prob
        if random.random() < self.mutation_prob:
            new_pattern = set(individual.pattern)

            # Decide to add or remove a cell
            if random.random() < 0.5 and new_pattern:  # Remove an existing cell
                new_pattern.remove(random.choice(list(new_pattern)))
            else:  # Add a new cell within grid bounds
                new_cell = (random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1))
                if len(new_pattern) < self.max_cells:
                    new_pattern.add(new_cell)

            # Ensure the pattern respects the max_cells constraint
            if len(new_pattern) > self.max_cells:
                new_pattern = set(list(new_pattern)[:self.max_cells])

            return LifeGrid(new_pattern, self.grid_size)

        # Return the original individual if no mutation occurs
        return individual

    def next_generation(self):
        # Sort the population based on fitness
        sorted_population = sorted(self.population, key=lambda ind: self.get_fitness(ind), reverse=True)

        # Calculate the size of the elite group (top 10% of population)
        elite_size = max(1, int(0.1 * len(self.population)))  # Ensure at least 1 elite individual
        elite_group = sorted_population[:elite_size]

        # Split the elite group into the top 50% and bottom 50%
        top_elite_size = elite_size // 2  # Top 50% of elite
        top_elite = elite_group[:top_elite_size]
        bottom_elite = elite_group[top_elite_size:]

        # Initialize the next generation with the top 50% of elite individuals
        next_gen = deepcopy(top_elite)

        # Crossover bottom 50% of elite with remaining individuals
        non_elite_population = sorted_population[elite_size:]
        while len(next_gen) < len(self.population):  # Maintain population size
            # Randomly select a bottom elite and a non-elite individual for crossover
            parent1 = random.choice(bottom_elite)
            parent2 = random.choice(non_elite_population)

            # Perform crossover to generate children
            child1, child2 = self.crossover(parent1, parent2)

            # Perform mutation on children
            child1 = self.mutation(child1)
            child2 = self.mutation(child2)

            # Add children to the next generation (ensure population size isn't exceeded)
            next_gen.append(child1)
            if len(next_gen) < len(self.population):
                next_gen.append(child2)

        # Update the population with the new generation
        self.population = next_gen


if __name__ == "__main__":
    # Initialize the Genetic Algorithm
    ga = GeneticAlgorithm(pop_size=200, grid_size=20, gen_limit=300, threshold_fit=100)

    # Find Methuselah
    methuselah = ga.find_methuselah()

    if methuselah[0]:
        print(f"Found Methuselah pattern with fitness {methuselah[1]}!")

        # Save Methuselah pattern to a TOML file
        save_to_toml(methuselah[0].pattern, methuselah[1])
    else:
        print("No Methuselah pattern found within generation limit.")

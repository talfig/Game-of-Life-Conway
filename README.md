# Game-of-Life Simulation with Genetic Algorithm

This project simulates the "Game of Life" using a grid, and employs a genetic algorithm to evolve configurations. The goal is to evolve a grid pattern that can evolve into a "Methuselah" (a pattern that lasts for many generations before reaching a stable state).

## Project Structure

The project is organized into several modules, each responsible for different parts of the simulation:

- **grid.py**: Contains the `LifeGrid` class, which models the grid and manages the evolution of cell patterns based on the Game of Life rules.
- **genetic_algorithm.py**: Implements the genetic algorithm to evolve LifeGrid patterns towards a Methuselah state.
- **simulation.py**: Runs simulations of LifeGrid evolution and tracks the maximum size of patterns.
- **pattern.py**: Handles saving and loading patterns to/from TOML files.
- **gui_simulation.py**: Provides a GUI interface using `tkinter` to visually simulate the Game of Life.

Each module encapsulates specific functionality like grid management, genetic algorithm operations, pattern handling, and visualization through a graphical interface.

## How It Works

### 1. Genetic Algorithm
The genetic algorithm works by initializing a population of random `LifeGrid` configurations. Each individual grid's fitness is calculated by running a simulation and measuring the maximum size the pattern reaches. The algorithm selects the fittest individuals for reproduction using crossover and mutation to generate the next generation. The goal is to evolve a grid pattern that exceeds a certain fitness threshold (Methuselah).

### 2. Simulation
The `LifeGrid` class is the core of the simulation. It applies the Game of Life rules to evolve a pattern. The grid evolves by checking the number of neighbors for each cell and deciding whether the cell survives or dies based on the classic Game of Life rules.

### 3. Visualization
A simple `tkinter` GUI displays the simulation in real time. The `GuiSimulation` class creates a grid of cells, where each cell is either alive (black) or dead (white). The simulation can be started and stopped with buttons, and the current generation and number of alive cells are displayed.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/game-of-life-conway.git
   ```

2. Install dependencies:
   ```bash
   pip install toml
   ```

## Usage

To run the genetic algorithm and find a Methuselah pattern, you can execute the `genetic_algorithm.py` script:

bash
Copy code

```bash
python rplife/genetic_algorithm.py
```

To run the GUI simulation:

```bash
python rplife/gui_simulation.py
```

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/talfig/Game-of-Life-Conway/blob/main/LICENSE) file for details.

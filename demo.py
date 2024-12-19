import rplife
import time


# Define a function to load a pattern and run the GUI simulation
def run_simulation(pattern_name, grid_size=20, cell_size=20, refresh_rate=50):
    """
    Run a GUI simulation with a specific pattern.

    Args:
        pattern_name (str): The name of the pattern to load.
        grid_size (int): The size of the grid for the simulation.
        cell_size (int): The size of each cell in the GUI.
        refresh_rate (int): The refresh rate of the GUI in milliseconds.
    """
    # Load the alive cells from the pattern
    alive_cells = rplife.load_from_toml(file_name="rplife/patterns.toml", pattern_name=pattern_name)

    # Convert the alive cells to a set of tuples
    alive_cells_set = set(tuple(cell) for cell in alive_cells)

    # Initialize the LifeGrid
    life = rplife.LifeGrid(pattern=alive_cells_set, grid_size=grid_size)

    # Run the GUI simulation
    print(f"Running simulation for pattern: {pattern_name}")
    rplife.GuiSimulation(life=life, cell_size=cell_size, refresh_rate=refresh_rate)


if __name__ == "__main__":
    # List of patterns to simulate
    patterns = ["9:131", "8:118", "10:122", "10:126", "7:105"]

    # Sequentially run each simulation
    for pattern in patterns:
        run_simulation(pattern_name=pattern)

        # Pause briefly between simulations
        print(f"Finished simulation for pattern: {pattern}")
        time.sleep(1)

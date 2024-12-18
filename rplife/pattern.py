# rplife/patterns.py

import toml


def save_to_toml(methuselah_pattern, methuselah_fitness, file_name="patterns.toml"):
    """
    Save the Methuselah pattern to a TOML file with a dynamic section name.

    Args:
        methuselah_pattern (set): The Methuselah pattern as a set of (x, y) tuples.
        methuselah_fitness (int/float): The fitness value of the Methuselah pattern.
        file_name (str): The name of the TOML file to save the pattern to.
    """
    if not methuselah_pattern:
        print("No Methuselah pattern to save.")
        return

    # Convert the pattern to a list of lists
    alive_cells = [list(cell) for cell in methuselah_pattern]

    # Generate the section name dynamically based on size and fitness
    section_name = f"{len(methuselah_pattern)}:{methuselah_fitness}"

    # Create a dictionary for TOML format
    data = {
        section_name: {
            "alive_cells": alive_cells
        }
    }

    # Write the data to a TOML file
    with open(file_name, "a+", encoding="utf-8") as toml_file:
        toml_string = toml.dumps(data)  # Generate the TOML string
        toml_file.write(toml_string)  # Write the string to the file

    print(f"Methuselah pattern saved to {file_name}.")

# rplife/gui_simulation.py

import copy
import tkinter as tk
from grid import LifeGrid


class GuiSimulation:
    def __init__(self, life: LifeGrid, cell_size=10, refresh_rate=50, spoiler_text=None):
        self.start_button = None
        self.stop_button = None
        self.life = copy.deepcopy(life)
        self.rows = life.end_row
        self.cols = life.end_col
        self.cell_size = cell_size
        self.refresh_rate = refresh_rate
        self.spoiler_text = spoiler_text

        self.alive_color = 'black'
        self.dead_color = 'white'
        self.gen = 0

        self.canvas_cells = [[0] * self.cols for _ in range(self.rows)]
        self.root = tk.Tk()
        self.root.title('Game of Life')

        self.running = False  # To track the running state of the simulation

        # Create a frame to hold the labels at the top
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # Create the labels for Generation and Alive Cells
        self.label = tk.Label(self.top_frame, text=self.get_label_text(), font="bold")
        self.label.pack(anchor='center', pady=5)

        if self.spoiler_text:
            self.sub_label = tk.Label(self.top_frame, text=self.spoiler_text)
            self.sub_label.pack(anchor='center')

        # Create the canvas after initializing the frame
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg='white')
        self.canvas.pack()

        # Create a frame to hold the buttons at the bottom
        self.bottom_frame = tk.Frame(self.root)
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Create Start and Stop buttons
        self.create_buttons()

        self.root.resizable(False, False)
        self.create_canvas()  # Create the grid canvas

        self.root.mainloop()

    def update_label(self):
        self.label.config(text=self.get_label_text())

    def get_label_text(self):
        # Get the number of alive cells
        alive_cells_count = len(self.life.pattern)
        return f"Generation: {self.gen}  Alive Cells: {alive_cells_count}"

    def create_canvas(self):
        for y in range(self.rows):
            for x in range(self.cols):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                # Fill all canvas cells in dead color by default
                canvas_square_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.dead_color, outline="black")
                self.canvas_cells[y][x] = canvas_square_id

        self.update_canvas(self.life.pattern)

    def update_canvas(self, live):
        # Update live cells
        for y in range(self.rows):
            for x in range(self.cols):
                canvas_square_id = self.canvas_cells[y][x]
                if (y, x) in live:
                    self.canvas.itemconfig(canvas_square_id, fill=self.alive_color)
                else:
                    self.canvas.itemconfig(canvas_square_id, fill=self.dead_color)

    def create_buttons(self):
        # Use grid layout to center the buttons
        self.bottom_frame.columnconfigure(0, weight=1)  # Empty column on the left
        self.bottom_frame.columnconfigure(1, weight=1)  # Start button column
        self.bottom_frame.columnconfigure(2, weight=1)  # Stop button column
        self.bottom_frame.columnconfigure(3, weight=1)  # Empty column on the right

        # Create Start and Stop buttons
        self.start_button = tk.Button(self.bottom_frame, text='Start', command=self.start_simulation)
        self.start_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(self.bottom_frame, text='Stop', command=self.stop_simulation)
        self.stop_button.grid(row=0, column=2, padx=5)

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.move_to_next_gen()

    def stop_simulation(self):
        self.running = False

    def move_to_next_gen(self, *args):
        if self.running:
            self.gen += 1
            self.life.evolve()
            updated_pattern = set(self.life.pattern)

            self.update_canvas(updated_pattern)
            self.update_label()

            # Re-call the function after the refresh rate interval
            self.root.after(self.refresh_rate, self.move_to_next_gen)


if __name__ == "__main__":
    # Example list of alive cells
    alive_cells = [
        [5, 10], [5, 11], [7, 7], [4, 8],
        [5, 8], [11, 13], [5, 9], [17, 3]
    ]

    # Convert the alive cells to a set of tuples
    alive_cells_set = set(tuple(cell) for cell in alive_cells)

    # Define the grid size
    grid_size = 20  # Adjust the size as needed for the grid

    # Initialize the LifeGrid
    life = LifeGrid(pattern=alive_cells_set, grid_size=grid_size)

    # Run the GUI simulation
    GuiSimulation(life=life, cell_size=20, refresh_rate=50)

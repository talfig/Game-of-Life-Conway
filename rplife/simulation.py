# rplife/simulation.py

import copy
from grid import LifeGrid


class Simulation:
    def __init__(self, life: LifeGrid, gen_limit=400):
        self.life = copy.deepcopy(life)

        self.gen = 0
        self.gen_limit = gen_limit

        self.size = self.life.get_size()
        self.max_size = self.size
        self.max_size_gen = self.gen
        self.gen_history = []

    def simulate(self):
        while self.gen <= self.gen_limit and not self.stabilized():
            self.gen += 1

            self.gen_history.append(copy.deepcopy(self.life.pattern))
            self.life.evolve()
            self.update_size()

    def get_spoiler_text(self):
        line1 = "Simulation ended at gen {} and {}\n".format(self.gen, "stabilized" if self.stabilized() else "did not stabilized")
        line2 = "Max size will be {}, size will peak at gen {}".format(self.max_size, self.max_size_gen)
        return line1 + line2

    def stabilized(self):
        return self.life.pattern in self.gen_history

    def update_size(self):
        self.size = self.life.get_size()
        if self.size > self.max_size:
            self.max_size = self.size
            self.max_size_gen = self.gen

    def get_max_size(self):
        return self.max_size

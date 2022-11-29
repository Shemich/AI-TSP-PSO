from util import path_cost


class Particle:
    def __init__(self, path, cost=None):
        self.path = path
        self.cog_best = path
        self.current_cost = cost if cost else self.path_cost()
        self.cog_best_cost = cost if cost else self.path_cost()
        self.velocity = []

    def clear_velocity(self):
        self.velocity.clear()

    def update_costs_and_cog_best(self):
        self.current_cost = self.path_cost()
        if self.current_cost < self.cog_best_cost:
            self.cog_best = self.path
            self.cog_best_cost = self.current_cost

    def path_cost(self):
        return path_cost(self.path)

import itertools
import time

from util import read_cities, path_cost, visualize_tsp


class BruteForce:
    def __init__(self, cities):
        self.cities = cities

    def run(self):
        self.cities = min(itertools.permutations(self.cities), key=lambda path: path_cost(path))
        return path_cost(self.cities)


if __name__ == "__main__":

    brute = BruteForce(read_cities(12))
    start = time.time()
    brute.run()
    end = time.time() - start
    print(f'Стоимость: {path_cost(brute.cities)}\t| Время: {round(end, 12)}')

    visualize_tsp('Полный перебор TSP', brute.cities)

import random
import time

import matplotlib.pyplot as plt

from particle import Particle
from util import read_cities, visualize


class PSO:

    def __init__(self, iterations, particles_count, soc=1.0, cog=1.0, cities=None, verbose=True):
        self.cities = cities
        self.soc_best = None
        self.soc_cost_iter = []
        self.iterations = iterations
        self.particles_count = particles_count
        self.particles = []
        self.soc = soc
        self.cog = cog
        self.verbose = verbose

        if self.verbose:
            print()
            print("------------------ ПАРАМЕТРЫ -----------------")
            print("Число городов:", len(self.cities))
            print("Число итераций:", self.iterations)
            print("Число частиц:", self.particles_count)
            print("cog: {}\tsoc: {}".format(self.cog, self.soc))
            print()
            print("----------------- ОПТИМИЗАЦИЯ ----------------")
            print("Инициализация...")
        solutions = self.init_particles()
        self.particles = [Particle(path=i) for i in solutions]

    # возвращает рандомный маршрут по городам
    def random_path(self):
        return random.sample(self.cities, len(self.cities))

    def init_particles(self):
        random_population = [self.random_path() for _ in range(self.particles_count - 1)]
        greedy_population = [self.greedy_path(0)]
        return [*random_population, *greedy_population]

    def greedy_path(self, start_index):
        unvisited = self.cities[:]
        del unvisited[start_index]
        path = [self.cities[start_index]]
        while len(unvisited):
            index, nearest_city = min(enumerate(unvisited), key=lambda item: item[1].distance(path[-1]))
            path.append(nearest_city)
            del unvisited[index]
        return path

    def run(self):
        start = time.time()
        self.soc_best = min(self.particles, key=lambda p: p.cog_best_cost)
        print(f"Cтоимость после инициализации: {self.soc_best.cog_best_cost}")

        if self.verbose:
            print("Начало оптимизации...")
        plt.ion()
        plt.draw()
        for i in range(self.iterations):
            self.soc_best = min(self.particles, key=lambda p: p.cog_best_cost)
            # Чтобы посмотреть рилтайм изменения
            if i % 10 == 0:
                visualize(self, pso, i)
            self.soc_cost_iter.append(self.soc_best.cog_best_cost)

            for particle in self.particles:
                particle.clear_velocity()
                temp_velocity = []
                soc_best = self.soc_best.cog_best[:]
                new_path = particle.path[:]

                for i in range(len(self.cities)):
                    if new_path[i] != particle.cog_best[i]:
                        swap = (i, particle.cog_best.index(new_path[i]), self.cog)
                        temp_velocity.append(swap)
                        new_path[swap[0]], new_path[swap[1]] = \
                            new_path[swap[1]], new_path[swap[0]]

                for i in range(len(self.cities)):
                    if new_path[i] != soc_best[i]:
                        swap = (i, soc_best.index(new_path[i]), self.soc)
                        temp_velocity.append(swap)
                        soc_best[swap[0]], soc_best[swap[1]] = soc_best[swap[1]], soc_best[swap[0]]

                particle.velocity = temp_velocity

                for swap in temp_velocity:
                    if random.random() <= swap[2]:
                        new_path[swap[0]], new_path[swap[1]] = \
                            new_path[swap[1]], new_path[swap[0]]

                particle.path = new_path
                particle.update_costs_and_cog_best()
        if self.verbose:
            time.sleep(0.2)
            print("Конец оптимизации...")
            print()
            print("------------------- РЕЗУЛЬТАТЫ -------------------")
        end = time.time() - start
        print(f'Стоимость: {pso.soc_best.cog_best_cost}\t| Время: {round(end, 2)}')
        print(f'Маршрут: {pso.soc_best.cog_best}')


if __name__ == "__main__":
    sum = 0
    cities_count = 10
    cities = read_cities(cities_count)
    i = 0
    repeat = 1
    while i < repeat:
        pso = PSO(iterations=1000, particles_count=300, cog=0.9, soc=0.1, cities=cities, verbose=True)
        pso.run()
        x_list, y_list = [], []
        for city in pso.soc_best.cog_best:
            x_list.append(city.x)
            y_list.append(city.y)
        x_list.append(pso.soc_best.cog_best[0].x)
        y_list.append(pso.soc_best.cog_best[0].y)

        fig = plt.figure(1)
        fig.suptitle('МРЧ задача Коммивояжёра')
        plt.plot(x_list, y_list, 'r')
        plt.plot(x_list, y_list)
        plt.show()
        plt.pause(20)
        i = i + 1
        sum = sum + pso.soc_best.cog_best_cost

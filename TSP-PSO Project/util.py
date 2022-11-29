import math

import matplotlib.pyplot as plt


class City:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # вычисляет гипотенузу треугольника с катетами X и Y (дистанцию)
    def distance(self, city):
        return math.hypot(self.x - city.x, self.y - city.y)

    def __repr__(self):
        return f"({self.x}, {self.y})"


def read_cities(size):
    cities = []
    with open(f'data/cities_{size}.data', 'r') as handle:
        lines = handle.readlines()
        for line in lines:
            x, y = map(float, line.split())
            cities.append(City(x, y))
    return cities


def path_cost(path):
    return sum([city.distance(path[index - 1]) for index, city in enumerate(path)])


def visualize_tsp(title, cities):
    fig = plt.figure()
    fig.suptitle(title)
    x_list, y_list = [], []
    for city in cities:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(cities[0].x)
    y_list.append(cities[0].y)
    plt.plot(x_list, y_list, 'ro')
    plt.plot(x_list, y_list, 'b')
    datafile = 'img/russia.jpg'
    img = plt.imread(datafile)
    plt.imshow(img, zorder=0, extent=[0, 795, 0, 447])
    plt.show()


def visualize(self, pso, i):
    plt.figure(0)
    plt.plot(pso.soc_cost_iter, 'b')
    plt.ylabel('Расстояние')

    plt.xlabel('Кол-во итераций')
    fig = plt.figure(0)
    fig.suptitle('PSO')
    x_list, y_list = [], []
    for city in self.soc_best.cog_best:
        x_list.append(city.x)
        y_list.append(city.y)
    x_list.append(pso.soc_best.cog_best[0].x)
    y_list.append(pso.soc_best.cog_best[0].y)
    fig = plt.figure(1)
    fig.clear()
    fig.suptitle(f'PSO TSP (кол-во итераций {i})')
    plt.xlabel('Позиция узла по X')
    plt.ylabel('Позиция узла по Y')
    plt.plot(x_list, y_list, 'b')
    datafile = 'img/russia.jpg'
    img = plt.imread(datafile)
    plt.imshow(img, zorder=0, extent=[0, 795, 0, 447])
    plt.draw()
    plt.pause(.0001)

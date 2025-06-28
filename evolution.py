from dataclasses import dataclass
import random

import numpy as np


@dataclass
class SquarePlaceData:
    x: float
    y: float
    length: int 


@dataclass
class CircleSquaresData:
    M: int
    squares: list[SquarePlaceData]


class Darwin:
    def __init__(self, r, K, crossing_alpha, mutation_sigma,
                 tournament_size, crossing_p, mutation_p, generations_count, population_size,
                 float_error=1e-9):
        self.r = r
        self.K = K
        self.crossing_alpha = crossing_alpha
        self.mutation_sigma = mutation_sigma
        self.tournament_size = tournament_size
        self.crossing_p = crossing_p
        self.mutation_p = mutation_p
        self.generations_count = generations_count
        self.population_size = population_size
        self.float_error = float_error

    def f(self, x, h):
        if h <= 0 or self.r**2 - x**2 <= 0:
            return 0 
        return int(
            2*(self.r**2 - x**2)**0.5/h
        )

    def g(self, x0, x1, h):
        if abs(self.r - abs(x0)) <= abs(self.r - abs(x1)):
            return self.f(x0, h)
        return self.f(x1, h)


    def generate_p(self, h):
        x0 = (-(4*self.r**2 - h**2)**0.5)/2 + self.float_error
        while x0 + h <= self.r:
            yield x0, x0 + h
            x0 += h

    def M(self, h):
        m = 0
        squares = []
        for x0, x1 in self.generate_p(h):
            g_val = self.g(x0, x1, h)
            m += g_val
            squares.append(
                SquarePlaceData(
                    x0, -(self.r**2 - max(x0**2, x1**2))**0.5, g_val
                )
            )
            if m >= self.K:
                squares[-1].length -= (m - self.K)
                m = self.K
                break
        return CircleSquaresData(self.K*h**2 if m == self.K else 0, squares)


    def crossing(self, h1, h2):
        h1, h2 = min(h1, h2), max(h1, h2)
        s, e = max(0, h1 - self.crossing_alpha*(h2 - h1)), min(2**0.5*self.r, h2 + self.crossing_alpha*(h2 - h1))
        return random.uniform(s, e), random.uniform(s, e)

    def mutation(self, h):
        # return random.triangular(0, 2**0.5*self.r, random.gauss(h, self.mutation_sigma))
        return max(self.float_error, min(2**0.5 * self.r, random.gauss(h, self.mutation_sigma)))

    def selection(self, population, population_mark):
        new = []
        for _ in range(len(population)):
            idxs = [random.randint(0, len(population) - 1) for __ in range(self.tournament_size)]
            new.append(population[max(idxs, key=lambda i: population_mark[i])])
        return new

    def next_population(self, population, population_mark):
        new = self.selection(population, population_mark)
        parents = [i for i in range(len(new)) if random.random() < self.crossing_p]
        for i in range(0, len(parents), 2):
            new[i], new[i + 1] = self.crossing(new[i], new[i + 1])
        for i in range(len(new)):
            if random.random() < self.mutation_p:
                new[i] = self.mutation(new[i])
        return new

    def solve(self):
        population = list(map(float, np.linspace(0, (2**0.5)*self.r, num=self.population_size + 1)[1:]))
        M = [self.M(h) for h in population]
        population_mark = [m.M for m in M]
        #yield population
        yield population, M
        for _ in range(self.population_size - 1):
            population = self.next_population(population, population_mark)
            M = [self.M(h) for h in population]
            population_mark = [m.M for m in M]
            yield population, M
            #yield population
        yield population[max(range(len(population)), key=lambda i: M[i].M)]


if __name__ == "__main__":
    darwin = Darwin(5, 2, 0.5, 2, 2, 0.7, 0.2, 10, 100)
    # for x in darwin.solve():
    #     print(x)
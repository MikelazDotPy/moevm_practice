from dataclasses import dataclass, InitVar
from functools import lru_cache
import random

import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np


min_h = 4e-3


class Creature:
    def __init__(self, h: float, r: float, R: float) -> None:
        self.R = R
        self.h = max(self.R*min_h, min(2**0.5 * R, h))
        self.r = min(R, max(r, ((4*R**2 - self.h**2)**0.5)/2))
    
    def __repr__(self) -> str:
        return f"h={self.h} r={self.r}"

    def __setattr__(self, name, value) -> None:
        if name == "h":
            object.__setattr__(self, "h", max(self.R*min_h, min(2**0.5 * self.R, value)))
        elif name == "r":
            object.__setattr__(self, "r", min(self.R, max(value, ((4*self.R**2 - self.h**2)**0.5)/2)))
        elif name == "R":
            object.__setattr__(self, "R", value)
        else:
            object.__setattr__(self, name, value)


class Darwin:
    def __init__(self, R: float, K: int, P_m: float,
                 sigma: float, P_c: float, alpha: float,
                 c: int, N: int, n: float, m: int, D: int, E: int, eps: float) -> None:
        self.R: float = max(0, R)
        self.K: int = max(1, int(K))

        self.P_m: float = min(1, max(0, P_m))
        self.sigma: float = max(0, sigma)

        self.P_c: float = min(1, max(0, P_c))
        self.alpha: float = max(0, alpha)
        self.c: int = max(0, int(c))

        self.N: int = max(1, int(N))
        self.n: int = int(self.N*min(1, max(0, n)))
        self.m: int = max(2, int(m))
        self.D: int = max(1, int(D))
        self.E: int = max(1, int(E))
        self.eps: float = max(0, eps)

    @lru_cache(None)
    def f(self, x: float, h: float) -> int:
        return int(
            (2*(self.R**2 - x**2)**0.5)/h
        )
    
    @lru_cache(None)
    def g(self, x0: float, x1: float, h: float) -> int:
        if self.R - abs(x0) <= self.R - abs(x1):
            return self.f(x0, h)
        return self.f(x1, h)
    
    @lru_cache(None)
    def get_ro(self, r: float, h: float) -> tuple[float]:
        return tuple(map(float, np.arange(-r, self.R, h)))

    @lru_cache(None)
    def M_(self, h: float, r: float) -> int:
        ro = self.get_ro(r, h)
        return sum(
            self.g(ro[i], ro[i + 1], h)
            for i in range(len(ro) - 1)
        )
    
    @lru_cache(None)
    def M(self, h: float, r: float) -> float:
        M_ = self.M_(h, r)
        if M_ >= self.K:
            return h**2*self.K
        return 0

    def mutate(self, t: float) -> float:
        return random.gauss(t, self.sigma)
    
    def crossing(self, p1: Creature, p2: Creature) -> tuple[Creature]:
        h1, h2 = min(p1.h, p2.h), max(p1.h, p2.h)
        T_h = (h1 - self.alpha*(h2 - h1), h2 - self.alpha*(h2 - h1))
        r1, r2 = min(p1.r, p2.r), max(p1.r, p2.r)
        T_r = (r1 - self.alpha*(r2 - r1), r2 - self.alpha*(r2 - r1))
        return tuple(
            Creature(np.random.uniform(*T_h), np.random.uniform(*T_r), self.R)
            for _ in range(self.c)
        )
    
    def get_start_generation(self) -> list[Creature]:
        n = int(self.N**0.5)
        h_vars = (self.R*min_h, 2**0.5 * self.R + self.R*min_h)
        r_vars = (self.R*min_h, self.R)
        H = map(float, np.linspace(*h_vars, n))
        R = map(float, np.linspace(*r_vars, n))
        generation: list[Creature] = []
        for h in H:
            for r in R:
                generation.append(Creature(h, r, self.R))
        for _ in range(self.N - n**2):
            generation.append(Creature(random.uniform(*h_vars), random.uniform(*r_vars), self.R))
        generation.sort(key=lambda x: self.M(x.h, x.r), reverse=True)
        return generation
    
    def get_next_generation(self, generation: list[Creature]) -> list[Creature]:
        generation = generation[:]
        parents = [i for i in range(len(generation)) if random.random() < self.P_c]
        for i in range(len(parents) - 1):
            for j in range(i + 1, len(parents)):
                generation.extend(self.crossing(generation[parents[i]], generation[parents[j]]))
        # for i in range(len(parents)):
        #     generation.extend(self.crossing(generation[parents[i]], generation[parents[random.randint(0, len(parents) - 1)]]))
        for i in range(len(generation)):
            if random.random() < self.P_m:
                generation[i].h = self.mutate(generation[i].h)
            if random.random() < self.P_m:
                generation[i].r = self.mutate(generation[i].r)
        generation.sort(key=lambda x: self.M(x.h, x.r), reverse=True)
        new = generation[:self.n]
        for _ in range(self.N - self.n):
            idxs = [random.randint(0, len(generation) - 1) for __ in range(self.m)]
            new.append(generation[max(idxs, key=lambda i: self.M(generation[i].h, generation[i].r))])
        new.sort(key=lambda x: self.M(x.h, x.r), reverse=True)
        return new

    def solve(self) -> float:
        generation = self.get_start_generation()
        for _ in range(self.D - 1):
            generation = self.get_next_generation(generation)
        return generation[0]
    
    def solve_generator(self):
        generation = self.get_start_generation()
        for _ in range(self.D - 1):
            yield generation
            generation = self.get_next_generation(generation)
        yield generation
    
    def draw_squares_in_circle(self, creature: Creature):
        fig, ax = plt.subplots(figsize=(8, 8))
        ro = self.get_ro(creature.r, creature.h)
        print(ro, creature.r)
        
        k = 0
        for i in range(len(ro) - 1):
            x0, x1 = ro[i], ro[i + 1]
            y = -(self.R**2 - max(x0**2, x1**2))**0.5
            for j in range(min(self.g(x0, x1, creature.h), self.K - k)):
                ax.add_patch(
                    patches.Rectangle(
                    (x0, y + creature.h*j), creature.h, creature.h,
                    linewidth=1, edgecolor='red', facecolor='none'
                )
                )
                k += 1
            if k == self.K:
                break

        ax.add_patch(plt.Circle((0, 0), self.R, fill=False, color='blue', linewidth=2))

        ax.set_xlim(-self.R - 1, self.R + 1)
        ax.set_ylim(-self.R - 1, self.R + 1)
        ax.set_aspect('equal')
        plt.grid(True)
        plt.title(f'Сторона квадрата h = {creature.h}\n Начало разбиения r = {creature.r}')

        plt.show()
    

if __name__ == "__main__":
    darwin = Darwin(
        R=5**0.5, K=12, P_m=0.4, sigma=1, P_c=0.6, alpha=0.5, c=2, N=50, n=0.3, m=4, D=10, E=10, eps=1
    )
    d = darwin.solve()
    print(d)
    darwin.draw_squares_in_circle(d)
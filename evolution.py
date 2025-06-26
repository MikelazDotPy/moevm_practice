import random


def crossing(h1, h2, a, r):
    h1, h2 = min(h1, h2), max(h1, h2)
    s, e = max(0, h1 - a*(h2 - h1)), min(2**0.5*r, h2 + a*(h2 - h1))
    return random.uniform(s, e), random.uniform(s, e)


def mutation(h, r, sigma):
    return random.triangular(0, 2**0.5*r, random.gauss(h, sigma))
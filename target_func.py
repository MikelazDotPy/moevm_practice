from dataclasses import dataclass


EPS = 1e-9


def f(x, r, h):
    return int(
        2*(r**2 - x**2)**0.5/h
    )


def g(x0, x1, r, h):
    if abs(r - abs(x0)) <= abs(r - abs(x1)):
        return f(x0, r, h)
    return f(x1, r, h)


def generate_p(r, h):
    x0 = (-(4*r**2 - h**2)**0.5)/2 + EPS
    while x0 + h <= r:
        yield x0, x0 + h
        x0 += h

#Нижний псевдо-интеграл Дарбу
def M(r, h):
    return sum(
        g(x0, x1, r, h)
        for x0, x1 in generate_p(r, h)
    )


@dataclass
class SquarePlaceData:
    x: float
    y: float
    length: int 


@dataclass
class CircleSquaresData:
    M: int
    squares: list[SquarePlaceData]


def debug_M(r, h, k):
    m = 0
    squares = []
    for x0, x1 in generate_p(r, h):
        g_val = g(x0, x1, r, h)
        m += g_val
        squares.append(
            SquarePlaceData(
                x0, -(r**2 - max(x0**2, x1**2))**0.5, g_val
            )
        )
        if m >= k:
            squares[-1].length -= (m - k)
            m = k
            break
    return CircleSquaresData(m, squares)
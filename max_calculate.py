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
    x0 = -(4*r**2 - h**2)**0.5/2 + EPS
    while x0 + h <= r:
        yield x0, x0 + h
        x0 += h


def M(r, h):
    return sum(
        g(x0, x1, r, h)
        for x0, x1 in generate_p(r, h)
    )


r = 4
h = 2**0.5*r - EPS
print(M(r, h))
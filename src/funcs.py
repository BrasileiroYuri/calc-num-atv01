from math import cos, e, sin


def f1(x):
    return (2 * x**4) + (4 * x**3) + (3 * x**2) - 10 * x - 15


def f2(x):
    return (x**5) - (2 * x**4) - (9 * x**3) + (22 * x**2) + (4 * x) - 24


def f3(x):
    return 5 * x**3 + x**2 - (e ** (1 - 2 * x)) + cos(x) + 20


def f4(x):
    return sin(x) * x + 4

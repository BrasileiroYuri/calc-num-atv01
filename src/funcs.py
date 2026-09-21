from math import cos, e, sin


def f1(x):
    return (2 * x**4) + (4 * x**3) + (3 * x**2) - 10 * x - 15


def f2(x):
    return (x**5) - (2 * x**4) - (9 * x**3) + (22 * x**2) + (4 * x) - 24


def f3(x):
    return 5 * x**3 + x**2 - (e ** (1 - 2 * x)) + cos(x) + 20


def f4(x):
    return sin(x) * x + 4A

#Derivadas para comparar com as númericas

def df1(x):
    return 8 * x**3 + 12 * x**2 + 6 * x - 10
 
 
def df2(x):
    return 5 * x**4 - 8 * x**3 - 27 * x**2 + 44 * x + 4
 
 
def df3(x):
    return 15 * x**2 + 2 * x + 2 * e ** (1 - 2 * x) - sin(x)
 
 
def df4(x):
    return sin(x) + x * cos(x)
 
 
DERIVADAS = {f1: df1, f2: df2, f3: df3, f4: df4}


eps = 1e-9
max_iter = 100


def newton(f, a, b):
    pass


def bisseccao(f, a, b):
    x = (a + b) / 2
    fx = f(x)
    if abs(fx) < eps and (b - a) < eps:
        return x
    elif f(a) * fx < 0:
        return bisseccao(f, a, x)
    else:
        return bisseccao(f, x, b)


def ponto_fixo(f, a, b):
    pass


def falsa_posicao(f, a, b):
    pass


def secante(f, a, b):
    pass


def custom(f, a, b):
    pass

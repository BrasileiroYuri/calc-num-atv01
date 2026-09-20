from problema import sinal

EPS = 1e-9
MAX_ITER = 100


def newton(f, a, b):
    pass


def bisseccao(f, a, b, eps=EPS, max_iter=MAX_ITER):
    fa = f(a)
    fb = f(b)
    if sinal(fa) * sinal(fb) >= 0:
        raise ValueError("f(a) e f(b) precisam ter sinais opostos")

    x = 0
    for k in range(1, max_iter + 1):
        x = (a + b) / 2
        fx = f(x)

        if abs(fx) < eps and (b - a) < eps:
            return x, k

        if sinal(fa) * sinal(fx) < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx

    return x, max_iter


def falsa_posicao(f, a, b, eps=EPS, max_iter=MAX_ITER):
    fa = f(a)
    fb = f(b)
    if sinal(fa) * sinal(fb) >= 0:
        raise ValueError("f(a) e f(b) precisam ter sinais opostos")

    x_anterior = a
    for k in range(1, max_iter + 1):
        x = (a * fb - b * fa) / (fb - fa)
        fx = f(x)

        if abs(fx) < eps and abs(x - x_anterior) < eps:
            return x, k

        if sinal(fa) * sinal(fx) < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
        x_anterior = x

    return x_anterior, max_iter


def ponto_fixo(f, a, b):
    pass


def secante(f, a, b):
    pass


def custom(f, a, b):
    pass

from dataclasses import dataclass
from itertools import pairwise
from math import floor

import matplotlib.pyplot as plt


def sinal(v):
    if v > 0:
        return 1
    if v < 0:
        return -1
    return 0


def tabelar(f, a, b, h):
    tabela = []
    n = floor((b - a) / h)
    for i in range(n + 1):
        x = a + i * h
        tabela.append((x, f(x)))
    if b - tabela[-1][0] > 1e-9:
        tabela.append((b, f(b)))
    return tabela


@dataclass
class Intervalo:
    a: float
    b: float
    status: str


class Problema:
    def __init__(self, f, a, b, h):
        self.f = f
        self.a = a
        self.b = b
        self.h = h
        self.tabela = tabelar(f, a, b, h)  # a tabela DO PROBLEMA: essa sim é estado

    def printar(self):
        print(f"{self.f.__name__}: de {self.a} até {self.b}, passo {self.h}")
        print(f"{'x':>10} | {'f(x)':>15}")
        print("-" * 28)
        for x, y in self.tabela:
            print(f"{x:>10.4f} | {y:>15.6f}")
        print()

    def plotar(self):
        plt.figure()
        n = 1000
        xs = [self.a + (self.b - self.a) * i / n for i in range(n + 1)]
        plt.plot(xs, [self.f(x) for x in xs], "b-", label="f(x)")
        plt.plot(
            [p[0] for p in self.tabela],
            [p[1] for p in self.tabela],
            "o--",
            color="gray",
            label="tabelamento",
        )
        plt.axhline(0, color="black", linewidth=0.8)
        plt.title(self.f.__name__)
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.grid(True)
        plt.legend()
        plt.savefig(f"imgs/{self.f.__name__}.png")
        plt.show()
        plt.close()

    def dydx(self, x, h=1e-8):
        return (self.f(x + h) - self.f(x)) / h

    def corolario(self, a, b, n=100):
        positivo = False
        negativo = False
        for i in range(n + 1):
            d = self.dydx(a + (b - a) * i / n)
            if d > 0:
                positivo = True
            if d < 0:
                negativo = True
        return not (positivo and negativo)

    def isolar(self, tabela=None, h=None, profundidade=0):
        if tabela is None:
            tabela = self.tabela
        if h is None:
            h = self.h

        intervalos = []
        for (x0, y0), (x1, y1) in pairwise(tabela):
            if y0 == 0:
                intervalos.append(Intervalo(x0, x0, "EXATA"))
            elif sinal(y0) * sinal(y1) < 0:
                if self.corolario(a=x0, b=x1):
                    intervalos.append(Intervalo(x0, x1, "UNICA"))
                elif profundidade < 5:
                    sub = tabelar(self.f, x0, x1, h / 10)
                    intervalos += self.isolar(sub, h / 10, profundidade + 1)
                else:
                    intervalos.append(Intervalo(x0, x1, "PELO_MENOS_UMA"))
        return intervalos

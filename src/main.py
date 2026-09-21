from funcs import f1, f2, f3, f4
from metodos import *
from problema import Problema

problemas = [
    Problema(f1, 0, 3, 0.6),
    Problema(f2, 0, 5, 0.7),
    Problema(f3, -5, 5, 0.5),
    Problema(f4, 1, 5, 0.5),
]

metodos = [newton, falsa_posicao, secante, bisseccao, custom, ponto_fixo]

if __name__ == "__main__":
    for p in problemas:
        p.printar()
        for intervalo in p.isolar():
            if intervalo.status == "UNICA":
                for metodo in metodos:
                    try:
                     resultado = metodo(p.f, intervalo.a, intervalo.b)
                     print(resultado)
                    except ValueError as erro:
                        print(f"{metodo.__name__}: ERRO: {erro}")
        p.plotar()

import sys
import time

from funcs import f1, f2, f3, f4
from metodos import *
from problema import Problema

problemas = [
    Problema(f1, 0, 3, 0.6),
    Problema(f2, 0, 5, 0.7),
    Problema(f3, -5, 5, 0.5),
    Problema(f4, 1, 5, 0.5),
]

metodos = {
    "newton": newton,
    "falsa_posicao": falsa_posicao,
    "secante": secante,
    "bisseccao": bisseccao,
    "custom": custom,
    "ponto_fixo": ponto_fixo,
}

if __name__ == "__main__":
    # python main.py            -> roda todos os métodos (equivale a "all")
    # python main.py all        -> roda todos os métodos
    # python main.py newton     -> roda só o ponto_fixo (roda só o ponto_fixo acima)
    escolha = sys.argv[1] if len(sys.argv) > 1 else "all"
    if escolha == "all":
        selecionados = metodos
    elif escolha in metodos:
        selecionados = {escolha: metodos[escolha]}
    else:
        sys.exit(f"Método '{escolha}' não existe. Opções: all, {', '.join(metodos)}")

    for p in problemas:
        p.printar()
        for intervalo in p.isolar():
            if intervalo.status == "UNICA":
                for nome, metodo in selecionados.items():
                    try:
                        # Tempo de processamento (sugestão do Guia de Laboratório
                        # 04), medido só em volta da chamada do método, sem
                        # contar impressão nem plotagem.
                        inicio = time.perf_counter()
                        resultado = metodo(p.f, intervalo.a, intervalo.b)
                        tempo = time.perf_counter() - inicio
                        if resultado is None:
                            print(f"{nome}: não implementado")
                            continue
                        x, k, convergiu = resultado
                        status = "OK" if convergiu else "NÃO CONVERGIU"
                        print(f"{nome}: x={x}, iteracoes={k}, {status}, tempo={tempo:.2e}s")
                    except ValueError as erro:
                        print(f"{nome}: ERRO: {erro}")
        p.plotar()

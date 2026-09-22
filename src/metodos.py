from funcs import DERIVADAS
from problema import dydx, dydx_central, sinal

EPS = 1e-9  # NOTE: precisão usada como critério de parada em todos os métodos; ajustável aqui.
MAX_ITER = 100  # NOTE: limite de iterações; 

# NOTE: derivada usada pelo Newton quando ninguém passa df explicitamente.
# Opções: "numerica" (progressiva, a pedida na atividade) ou "exata" (usa
# DERIVADAS, de funcs.py). Para comparar com a central, troque a dydx usada
# dentro de newton() (logo abaixo) por dydx_central.
DERIVADA_NEWTON = "numerica"

# Todo método devolve (x, k, convergiu):
#   x         -> aproximação da raiz
#   k         -> número de iterações usadas
#   convergiu -> True se o critério de parada foi satisfeito,
#                False se o método parou por outro motivo
#                (estourou max_iter, divergiu, ficou estagnado etc.)


def newton(f, a, b, eps=EPS, max_iter=MAX_ITER, df=None):
    # Método de Newton-Raphson: aproxima a raiz pela intersecção com o eixo x
    # da reta tangente a f em x_k. Segue da expansão de Taylor de 1ª ordem de
    # f em torno de x_k igualada a zero, o que dá a fórmula do slide/guia:
    #     x_(k+1) = x_k - f(x_k) / f'(x_k)
    # O chute inicial é o ponto médio do intervalo isolado [a, b], como no
    # pseudocódigo do Guia de Laboratório 04 (x_ = (a+b)/2).
    if df is None:
        # Sem df explícito, o padrão é definido pela constante
        # DERIVADA_NEWTON (acima): "numerica" usa dydx (progressiva, a
        # pedida na atividade); "exata" usa a derivada calculada na mão,
        # de funcs.py. Passar df=... na chamada sempre tem prioridade sobre
        # esta constante (útil para testes pontuais pelo terminal).
        if DERIVADA_NEWTON == "exata":
            df = DERIVADAS[f]
        else:
            def df(x):
                return dydx(f, x)

    x = (a + b) / 2
    for k in range(1, max_iter + 1):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-14:
            # Tangente quase horizontal: o passo f(x)/f'(x) explode. Esta é
            # justamente uma das fragilidades do método (pergunta do slide de
            # Newton): perto de raízes onde f' também se anula (ex.: raízes
            # múltiplas), o passo fica instável.
            raise ValueError(f"derivada praticamente nula em x = {x}")

        x_novo = x - fx / dfx

        if x_novo < a or x_novo > b:
            # Outra fragilidade: sem essa checagem, nada impede o Newton de
            # "pular" para fora do intervalo onde a raiz foi isolada (ou até
            # convergir para outra raiz). Aqui tratamos isso como erro, em
            # vez de deixar o método seguir sem controle.
            raise ValueError(f"Newton saiu do intervalo")

        # Critério de parada: passo pequeno e |f(x)| pequeno (o guia usa só
        # |f(x_)| < tol; aqui somamos o critério do passo por robustez).
        if abs(x_novo - x) < eps and abs(f(x_novo)) < eps:
            return x_novo, k, True
        x = x_novo

    return x, max_iter, False


def bisseccao(f, a, b, eps=EPS, max_iter=MAX_ITER):
    # Método da Bissecção: pelo Teorema do Anulamento (Bolzano), se f é
    # contínua e f(a)*f(b) < 0, existe ao menos uma raiz em [a, b]. A cada
    # passo o intervalo é dividido ao meio em x = (a+b)/2 e o sub-intervalo
    # que preserva a troca de sinal (f(a)*f(x) < 0) é mantido.
    fa = f(a)
    fb = f(b)
    if sinal(fa) * sinal(fb) >= 0:
        raise ValueError("f(a) e f(b) precisam ter sinais opostos")

    x = 0
    for k in range(1, max_iter + 1):
        x = (a + b) / 2
        fx = f(x)

        # Critério de parada combinando os dois vimos em aula:
        # |f(x)| < eps  e  (b-a) < eps
        if abs(fx) < eps and (b - a) < eps:
            return x, k, True

        if sinal(fa) * sinal(fx) < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx

    return x, max_iter, False


def falsa_posicao(f, a, b, eps=EPS, max_iter=MAX_ITER):
    # Método da Falsa Posição: como a Bissecção, mantém sempre um intervalo
    # [a, b] com f(a)*f(b) < 0. A diferença é a escolha do próximo ponto: em
    # vez do ponto médio, usa a raiz da reta secante que liga (a, f(a)) a
    # (b, f(b)) — isto é, interpolação linear entre os extremos:
    #     x = (a*f(b) - b*f(a)) / (f(b) - f(a))
    fa = f(a)
    fb = f(b)
    if sinal(fa) * sinal(fb) >= 0:
        raise ValueError("f(a) e f(b) precisam ter sinais opostos")

    x_anterior = a
    for k in range(1, max_iter + 1):
        x = (a * fb - b * fa) / (fb - fa)
        fx = f(x)

        if abs(fx) < eps and abs(x - x_anterior) < eps:
            return x, k, True

        if sinal(fa) * sinal(fx) < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx
        x_anterior = x

    return x_anterior, max_iter, False


def _phi(f, x, alpha=0.1):
    # phi(x) = x + alpha * f(x), o caso A(x) = alpha (constante) do Teorema
    # do Ponto Fixo: phi(x) = x + A(x) f(x), com phi(x) = x se e só se f(x) = 0.
    return x + alpha * f(x)


def _lerp_phi(f, x, alpha=0.03):
    # NOTE: forma alternativa de phi, interpolando entre x e x+f(x).
    return (1 - alpha) * x + alpha * (f(x) + x)


def ponto_fixo(f, a, b, eps=EPS, max_iter=MAX_ITER):
    # Método do Ponto Fixo: reescreve f(x) = 0 como phi(x) = x e itera
    # x_(k+1) = phi(x_k). Pelo teorema visto em aula, a convergência é
    # garantida se |phi'(x)| < M < 1 em [a, b].

    phi = _phi
    # NOTE: troque para phi = _lerp_phi se quiser testar a outra forma.

    dfafb = f(b) - f(a)

    # alpha é a inclinação da reta secante entre a e b: (a-b)/(f(b)-f(a)).
    # Com A(x) = alpha constante, phi'(x) = 1 + alpha*f'(x); escolher alpha
    # assim aproxima phi'(x) de um passo do tipo secante/Newton, o que ajuda
    # (mas não garante) que |phi'(x)| < 1 no intervalo.
    # NOTE: se a convergência não for satisfatória para alguma f, este alpha
    # isso pode ser calculado manalmente.
    alpha = 0.01 if dfafb == 0 else (a - b) / dfafb

    x = (a + b) / 2

    for i in range(1, max_iter + 1):

        if abs(x) > 1e10:
            # Guarda de divergência: sem garantia de |phi'(x)|<1, a iteração
            # pode afastar-se da raiz em vez de se aproximar. Essa é a
            # fragilidade central do método (pergunta do slide): a
            # convergência depende inteiramente da escolha de phi (aqui,
            # de alpha), e não há forma automática de garantir |phi'(x)|<1
            # para qualquer f sem informação extra sobre a função.
            return x, i, False

        new_x = phi(f, x, alpha=alpha)

        if abs(f(new_x)) < eps or abs(new_x - x) < eps:
            return new_x, i, True

        x = new_x

    return x, max_iter, False


def secante(f, a, b, eps=EPS, max_iter=MAX_ITER):
    # Método da Secante: um "Newton modificado" (como no slide) que troca a
    # derivada f'(x_k) pela inclinação da reta secante entre os dois últimos
    # pontos calculados, (f(x1)-f(x0))/(x1-x0), evitando calcular f' a cada
    # passo:
    #     x2 = x1 - f(x1) * (x1 - x0) / (f(x1) - f(x0))
    #
    # Diferença para a Falsa Posição: a Falsa Posição
    # sempre mantém um par a, b com f(a)*f(b) < 0 (garantindo a raiz entre
    # eles — mais segura, porém mais lenta), enquanto a Secante sempre usa
    # os DOIS ÚLTIMOS pontos calculados, mesmo que fiquem do mesmo lado da
    # raiz. Isso faz a Secante perder a garantia de manter a raiz dentro do
    # intervalo, mas converge mais rápido (ordem ~1,618, superlinear, contra
    # a convergência linear da Falsa Posição).
    x0, x1 = a, b
    f0, f1 = f(x0), f(x1)

    for i in range(1, max_iter + 1):
        df = f1 - f0

        if abs(df) < eps:
            # NOTE: f0 ≈ f1 deixaria a divisão abaixo instável; interrompe
            # aqui em vez de dividir por um número muito pequeno. 
            return x1, i, False

        x2 = x1 - f1 * (x1 - x0) / df
        f2 = f(x2)

        if abs(f2) < eps or abs(x2 - x1) < eps:
            return x2, i, True

        x0, x1 = x1, x2
        f0, f1 = f1, f2

    return x1, max_iter, False


def custom(f, a, b):
    pass

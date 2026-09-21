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


def _phi(f, x, alpha=0.1):
    return x + alpha * f(x)

def _lerp_phi(f, x, alpha=0.03):
    return (1 - alpha) * x + alpha * (f(x) + x)

def ponto_fixo(f, a, b, eps=EPS, max_iter=MAX_ITER):
    
    phi = _phi
    # phi = _lerp_phi # use esse se quiser usar o _lerp_phi, mas ele é meio ruim
    
    dfafb = f(b) - f(a)
    
    alpha = 0.01 if dfafb == 0 else (a - b) / dfafb
    # alpha = (a - b) / dfafb if f(b) > f(a) else 0.01 if dfafb == 0 else (b - a) / dfafb # use esse se quiser usar o _lerp_phi, mas ele é meio ruim

    
    x = (a + b) / 2
    
    for i in range(1, max_iter + 1):
    
        if abs(x) > 1e10:
            return x, i
        
        new_x = phi(f, x, alpha=alpha) # escolhi o alpha como (a - b) / (fb - fa) por ser um alpha bom, mas ele é praticamente o método de newton.
                                       # infelizmente esse foi o único que eu testei que teve resultados bons e não dependia de informação externa.
                                       
        if abs(f(new_x)) < eps or abs(new_x - x) < eps:
            return new_x, i
        
        x = new_x
    
    return x, max_iter

def secante(f, a, b, eps=EPS, max_iter=MAX_ITER):
        
    x0, x1 = a, b
    f0, f1= f(x0),f(x1)    
            
    for i in range(1, max_iter + 1):
        df = f1 - f0
        
        if abs(df) < eps:
            return x1, i
        
        x2 = x1 - f1 * (x1 - x0) / df # da pra substituir por um phi se quiser, deixaria o alpha igual a (x1, x0) / df e fazia x2 = phi(f, x1, (x1 - x0) / df), 
                                      # mas teria mt calculo desnecessário.
        f2 = f(x2)
        
        if abs(f2) < eps or abs(x2 - x1) < eps:
            return x2, i
        
        x0, x1 = x1, x2
        f0, f1 = f1, f2
    
    return x1, max_iter
    

def custom(f, a, b):
    pass

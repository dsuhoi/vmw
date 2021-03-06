import math as m

import sympy as sp
from app.programs.utils import params_algorithms, register_algorithms
from scipy.misc import derivative
from sympy.parsing.sympy_parser import parse_expr


def result(func):
    def wrapper(params):
        f_expr = parse_expr(params["function"])
        f = sp.lambdify("x", f_expr, "numpy")
        a, b = (float(x) for x in params["range"].split())
        e = float(params["e"])
        text = (
            "Аналитическое решение: $$x_{аналит.} = "
            + sp.latex(sp.solveset(f_expr, domain=sp.S.Reals))
            + "$$ Численное решение: $$x_{числ.} = "
        )
        result, num_iter = func(f, a, b, e)
        return text + f"{result}$$ Число итераций равно {num_iter}."

    register_algorithms(result, func, wrapper)
    return wrapper


params_algorithms(result, ["function", "range", "e"])


@result
def half_det(f, a, b, e):
    cnt = 0
    c = (b + a) / 2
    while not ((m.fabs((b - a) / 2) <= e) or m.isclose(f(c), 0)):
        cnt += 1
        if f(a) * f(c) > 0:
            a = c
        else:
            b = c
        c = (b + a) / 2
        if cnt > 1e6:
            break
    return c, cnt


@result
def simple_iter(f, a, _, e):
    cnt = 0
    v = 0.5
    sgn = lambda x: -1 if x < 0 else 1
    f_a = derivative(f, a, dx=e)
    alpha = -sgn(f_a) * v / (1 + m.fabs(f_a))
    x_, x = a, a + alpha * f(a)
    while m.fabs(x - x_) > e:
        cnt += 1
        x_ = x
        x += alpha * f(x_)
    return x, cnt

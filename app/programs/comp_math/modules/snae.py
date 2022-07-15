import math as m

import numpy as np
import sympy as sp
from app.programs.utils import register_algorithms
from scipy.misc import derivative
from scipy.optimize import fsolve
from sympy.parsing.sympy_parser import parse_expr


def result(func):
    def wrapper(params):
        var_str, *func_str = [row for row in params["functions"].split("\r\n")]
        func_list = [
            sp.lambdify(var_str.split(), parse_expr(row), "numpy") for row in func_str
        ]
        d0 = [float(x) for x in params["d0"].split()]
        text = (
            "Эталонное решение: $$x_{эталон.} = "
            + sp.latex(
                [
                    round(x, 5)
                    for x in fsolve(
                        lambda x: [f(*x) for f in func_list], d0, epsfcn=float(1e-8)
                    )
                ]
            )
            + "$$ Численное решение: $$x_{числ.} = "
        )
        result, num_iter = func(func_list, d0, float(params["e"]))
        return text + f"{sp.latex(result)}$$ Число итераций равно {num_iter}."

    register_algorithms(result, func, wrapper)
    return wrapper


def init_phi(func_list, d0, e):
    n = len(d0)
    f_0 = [
        derivative(
            lambda x: func_list[i](*[x if j == i else d0[j] for j in range(n)]),
            d0[i],
            dx=e,
        )
        for i in range(n)
    ]
    sign = lambda x: -1 if x < 0 else 1
    return [-sign(f_0[i]) * 0.5 / (1 + m.fabs(f_0[i])) for i in range(n)]


@result
def gaus_zeid(func_list, d0, e):
    n = len(d0)
    x_ = np.array(d0)
    lambd = init_phi(func_list, d0, e)

    def phi(t, i):
        return t[i] + lambd[i] * func_list[i](*t)

    x = x_.copy()
    tmp = x_.copy()
    cnt = 1
    for i in range(n):
        x[i] = phi(x_, i)
        x_[i] = x[i]

    while np.linalg.norm(x - tmp) > e:
        cnt += 1
        tmp = x_.copy()
        for i in range(n):
            x[i] = phi(x_, i)
            x_[i] = x[i]
        if cnt > 1e6:
            break
    return x, cnt

from scipy.misc import derivative
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import math as m
import matplotlib.pyplot as plt

def result(func):
    def wrapper(params):
        fig = plt.figure(figsize=(9,6))
        ax = fig.add_subplot()
        
        func_str, var_str = (x for x in params['function'].split(","))
        d0 = [float(x) for x in params['d0'].split()]
        dx = float(params['dx'])
        coord = float(params['coord'])

        var_s = var_str.split()
        f_2 = sp.lambdify(var_s, parse_expr(func_str.replace(var_s[1] + f"({var_s[0]})", var_s[1])), "numpy")
        x = sp.Symbol(var_s[0])
        f = sp.Function(var_s[1])
        
        equal = sp.Eq(f(x).diff(x), parse_expr(func_str))
        expr_full = sp.dsolve(equal, f(x))
        expr_res = sp.dsolve(equal, ics={f(d0[0]): d0[1]})
        expr_d0 = expr_res.subs(x, coord)
        text = "Аналитическое решение: $$" + sp.latex(expr_full) +\
        "$$$$" + sp.latex(expr_res) + f"\qquad {var_s[1]}({d0[0]}) = {d0[1]}" +\
        "$$$$" + sp.latex(expr_d0) + f"$$Численное решение: $${var_s[1]}({var_s[0]})"+"_{числ.} = "
        
        ax.set_xlabel(var_s[0])
        ax.set_ylabel(var_s[1] + f"({var_s[0]})")
        ax.grid(True)
        x = np.linspace(d0[0] - m.fabs(d0[0]), coord + m.fabs(coord), 200)
        df = sp.lambdify(var_s[0], expr_res.args[1], "numpy")
        ax.plot(x, df(x))
        
        result = func(f_2, d0, coord, dx)
        
        ax.scatter(coord, result, c='r', s=20)

        delta = m.fabs(expr_d0.args[1] - result)/m.fabs(result)
        return fig, text + f"{result}$$Относительная погрешность: $${delta}$$График:"
    return wrapper


def euler_method(next_y):
    def wrapper(f, d0, coord, dx):
        ys = []
        xs = np.arange(d0[0] + dx, coord + dx, dx)
        y = d0[1]
        for x in xs:
            ys.append(y)
            y = next_y(x, y)
        return ys
    return wrapper

@result
def mod_euler(f, d0, coord, dx):
    @euler_method
    def mod_euler_method(xi, yi):
        nonlocal f, dx
        h = dx/2
        k2 = dx * f(xi + h, yi + h * f(xi, yi))
        return yi + k2

    return mod_euler_method(f, d0, coord, dx)[-1]

@result
def euler_koshi(f, d0, coord, dx):
    @euler_method
    def euler_koshi_method(xi, yi):
        nonlocal f, dx
        k1 = dx*f(xi, yi)
        k2 = dx*f(xi + dx, yi + k1)
        return yi + 0.5*(k1 + k2)

    return euler_koshi_method(f, d0, coord, dx)[-1]


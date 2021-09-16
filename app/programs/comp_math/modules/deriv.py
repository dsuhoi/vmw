import scipy.misc as sc
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import numpy as np
import matplotlib.pyplot as plt

def result(func):
    def wrapper(params):
        fig = plt.figure(figsize=(9,6))
        ax = None
        f_str, var_str = params['function'].split(",")
        var = sp.symbols(var_str)
        if isinstance(var, tuple):
            ax = fig.add_subplot(111, projection='3d')
            ax.set_zlabel('z')
            ax.set_xlabel(var[0])
            ax.set_ylabel(var[1])
        else:
            ax = fig.add_subplot()
            ax.set_xlabel(var)
            ax.set_ylabel(f"f({var})")
        ax.grid(True)
        ax.legend()

        f_parse = parse_expr(f_str)
        f = sp.lambdify(var, f_parse, "numpy")

        result = func(f, var,  ax, f_parse, params)

        return fig, result
    return wrapper


def f_(f, x):
    return sc.derivative(f, x, dx=1e-8)

def f_k(f, x0, x):
    k = sc.derivative(f, x0, dx=1e-8)
    text = sp.latex(parse_expr(f"{round(k, 2)}*(x - {x0}) + {round(f(x0), 2)}"))
    return k*(x - x0) + f(x0), text

def f2_k(f, x0, y0, x, y):
    k_x = sc.derivative(lambda xn: f(xn, y0), x0, dx=1e-8)
    k_y = sc.derivative(lambda yn: f(x0, yn), y0, dx=1e-8)
    text = sp.latex(parse_expr(
        f"{round(k_x, 3)}*(x - {x0}) + {round(k_y, 3)}*(y - {y0}) + {round(f(x0, y0), 3)}"))
    return k_x*(x - x0) + k_y*(y - y0) + f(x0, y0), text

@result
def derivative(f, var, ax, f_parse, params):
    ranges = [[float(d) for d in r.split()] for r in
            params['ranges'].split(",")]
    n = int(params['n'])
    d0 = None
    if params['d0'] and params['d0']!='':
        d0 = [float(x) for x in params['d0'].split()]

    x = np.linspace(ranges[0][0], ranges[0][1], n)
    if isinstance(var, tuple):
        y = np.linspace(ranges[1][0], ranges[1][1], n)
        X, Y = np.meshgrid(x, y)
        ax.plot_surface(X, Y, f(X, Y), label=sp.latex(f_parse),
            cmap='inferno')
        res = "График построен."
        if d0:
            f2k, text = f2_k(f, d0[0], d0[1], X, Y)
            ax.plot_surface(X, Y, f2k, label=text)
            res = "Уравнение касательной плоскости: $$z = " + text + "$$"
    else:
        ax.plot(x, f(x), label=sp.latex(f_parse))
        ax.plot(x, f_(f, x), "r--", label=sp.latex(sp.diff(f_parse)))
        res = f"$$ f'({var}) = " + sp.latex(sp.diff(f_parse, var))
        if d0:
            fk, text = f_k(f, d0[0], x)
            ax.plot(x, fk, "y", label=text)
            res += f", f'({d0[0]}) = {round(f_(f, d0[0]), 3)}, $$Уравнение касательной: $$y = " + text
        res += "$$"
    return res + "График:"

import json

import numpy as np
import plotly
import plotly.graph_objects as go
import scipy.misc as sc
import sympy as sp
from app.programs.utils import params_algorithms, register_algorithms
from sympy.parsing.sympy_parser import parse_expr


def result(func):
    def wrapper(params):
        f_str, var_str = params["function"].split(",")
        var = sp.symbols(var_str)

        f_parse = parse_expr(f_str)
        f = sp.lambdify(var, f_parse, "numpy")

        fig, result = func(f, var, f_parse, params)
        fig.update_layout(width=1000, height=1000)
        graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        return graphJSON, result

    register_algorithms(result, func, wrapper)
    return wrapper


params_algorithms(result, {"iframe": True})


def f_(f, x):
    return sc.derivative(f, x, dx=1e-8)


def f_k(f, x0, x):
    k = sc.derivative(f, x0, dx=1e-8)
    text = sp.latex(parse_expr(f"{round(k, 2)}*(x - {x0}) + {round(f(x0), 2)}"))
    return k * (x - x0) + f(x0), text


def f2_k(f, x0, y0, x, y):
    k_x = sc.derivative(lambda xn: f(xn, y0), x0, dx=1e-8)
    k_y = sc.derivative(lambda yn: f(x0, yn), y0, dx=1e-8)
    text = sp.latex(
        parse_expr(
            f"{round(k_x, 3)}*(x - {x0}) + {round(k_y, 3)}*(y - {y0}) + {round(f(x0, y0), 3)}"
        )
    )
    return k_x * (x - x0) + k_y * (y - y0) + f(x0, y0), text


@result
def derivative(f, var, f_parse, params):
    ranges = [[float(d) for d in r.split()] for r in params["ranges"].split(",")]
    n = int(params["n"])
    d0 = None
    if params["d0"] and params["d0"] != "":
        d0 = [float(x) for x in params["d0"].split()]

    fig = go.Figure()
    res = str()

    x = np.linspace(ranges[0][0], ranges[0][1], n)
    if isinstance(var, tuple):
        y = np.linspace(ranges[1][0], ranges[1][1], n)
        X, Y = np.meshgrid(x, y)
        fig.add_trace(
            go.Surface(x=X, y=Y, z=f(X, Y), colorscale="Viridis", name=f"f({var})")
        )
        if d0:
            f2k, text = f2_k(f, d0[0], d0[1], X, Y)
            fig.add_trace(go.Surface(x=x, y=y, z=f2k, colorscale="Viridis", name=text))
            res += "Уравнение касательной плоскости: $$z = " + text + "$$"
    else:
        fig.add_trace(go.Scatter(x=x, y=f(x), name=f"f({var})"))
        fig.add_trace(go.Scatter(x=x, y=f_(f, x), name=f"f'({var})"))
        res = f"$$ f'({var}) = " + sp.latex(sp.diff(f_parse, var))
        if d0:
            fk, text = f_k(f, d0[0], x)
            fig.add_trace(go.Scatter(x=x, y=fk, name=text))
            res += (
                f", f'({d0[0]}) = {round(f_(f, d0[0]), 3)}, $$Уравнение касательной: $$y = "
                + text
            )
        res += "$$"
    return fig, res + "График:"

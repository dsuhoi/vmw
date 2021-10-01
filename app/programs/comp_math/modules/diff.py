from scipy.misc import derivative
from scipy.integrate import odeint
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
        x = np.linspace(d0[0], coord, 200)
        f_2 = sp.lambdify(var_s, parse_expr(func_str), "numpy")
        
        res_sc = odeint(lambda y, x: f_2(x, y), d0[1], x)
        
        text = f"Эталонное решение: $${var_s[1]}({var_s[0]})_" + "{эталон.} = " +\
        f"{res_sc[-1]}$$Численное решение: $${var_s[1]}({var_s[0]})"+"_{числ.} = "
        
        ax.set_xlabel(var_s[0])
        ax.set_ylabel(var_s[1] + f"({var_s[0]})")
        ax.grid(True)
        ax.plot(x, res_sc)
        
        result = func(f_2, d0, coord, dx)
        
        ax.scatter(coord, result, c='r', s=20)

        delta = m.fabs(res_sc[-1] - result)/m.fabs(result)
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
def euler(f, d0, coord, dx):
    @euler_method
    def _euler_method(xi, yi):
        nonlocal f, dx
        return yi + dx*f(xi, yi)

    return _euler_method(f, d0, coord, dx)[-1]

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

@result
def runge_kutt(f, d0, coord, dx):
    @euler_method
    def runge_kutt_method(xi, yi):
        nonlocal f, dx
        h2 = dx / 2
        k1 = f(xi, yi)
        k2 = f(xi + h2, yi + h2 * k1)
        k3 = f(xi + h2, yi + h2 * k2)
        k4 = f(xi + dx, yi + dx * k3)
        return yi + (dx / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
    return runge_kutt_method(f, d0, coord, dx)[-1]

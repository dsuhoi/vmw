import math as m

import numpy as np
import scipy.optimize as sc
import sympy as sp
from app.programs.utils import params_algorithms, register_algorithms
from scipy.misc import derivative
from sympy.parsing import parse_expr


def result(func):
    def wrapper(params):
        func_str, var_str = [x for x in params["function"].split(",")]
        f = sp.lambdify(var_str.split(), parse_expr(func_str), "numpy")
        d0 = np.array([float(x) for x in params["d0"].split()])
        dx = float(params["dx"])
        e = float(params["e"])

        min_x = sc.minimize(lambda x: f(*x), d0, tol=1e-8)
        min_res = f(*min_x.x)
        text = (
            "Эталонное решение: $$x_{эталон.} = "
            + f"{[round(x, 3) for x in min_x.x]}$$"
            + "$$f(x)_{эталон.} = "
            + f"{round(min_res, 3)}$$"
        )

        x, y, i = func(f, d0, dx, e)

        text += (
            "Численное решение: $$x_{числ.} = "
            + f"{[round(i,6) for i in x]}"
            + "$$$$f(x)_{числ.} = "
            + f"{round(y,6)}$$Число итераций равно {i}."
        )
        return text

    register_algorithms(result, func, wrapper)
    return wrapper


params_algorithms(result, ["function", "d0", "dx", "e"])


def R(f, x, i, d=0):
    return f(*[x[j] + d if i == j else x[j] for j in range(x.size)])


def R_(f, x, i, e):
    f_ = lambda xi: f(*[xi if i == j else x[j] for j in range(x.size)])
    return derivative(f_, x[i], dx=e)


@result
def gaus_zeid(f, d0, h, e):
    minimum = [d0.copy(), f(*d0)]
    cnt = 0
    while h > e:
        opt_flag = True
        for j in range(d0.size):
            cnt += 1
            Ra = 1, R(f, minimum[0], j, h)
            Rb = -1, R(f, minimum[0], j, -h)
            temp = min([Ra, Rb, minimum], key=lambda x: x[1])
            if temp[1] < minimum[1]:
                opt_flag = False
                d = temp[0]
                minimum[0][j] += d * h
                minimum[1] = temp[1]
                x = minimum[0].copy()
                while True:
                    x[j] += d * h
                    temp = f(*x)
                    if temp < minimum[1]:
                        minimum[0][j] = x[j]
                        minimum[1] = temp
                    else:
                        break

        if opt_flag:
            h /= 2
        else:
            opt_flag = True

        if cnt > 1e6:
            break

    return minimum[0].tolist(), minimum[1], cnt


@result
def relax(f, d0, h, e):
    minimum = [d0.copy(), f(*d0)]
    cnt = 0
    opt_flag = [False for x in range(d0.size)]
    while h > e:
        cnt += 1
        R_list = [R_(f, minimum[0], i, e) for i in range(d0.size)]
        r_min = R_list.index(max(R_list, key=lambda x: m.fabs(x)))
        if opt_flag[r_min] == True:
            h /= 2
            opt_flag[r_min] = False
        else:
            opt_flag[r_min] = True
        d = -1 if R_list[r_min] > 0 else 1
        x = minimum[0].copy()
        x[r_min] += d * h
        while True:
            x[r_min] += d * h
            temp = f(*x)
            if temp < minimum[1]:
                minimum[0][r_min] = x[r_min]
                minimum[1] = temp
            else:
                break

    return minimum[0].tolist(), minimum[1], cnt

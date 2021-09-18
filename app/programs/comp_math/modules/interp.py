import scipy.misc as sc
import numpy as np
import math as m
import matplotlib.pyplot as plt
from mpld3 import plugins

def result(func):
    def wrapper(params):
        fig = plt.figure(figsize=(9,6))
        ax = fig.add_subplot()
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.grid(True)
        line_colect = []
        coords = np.array([[float(x) for x in pair.split()] for pair in params['coords'].split("\r\n")])
        rng = [float(x) for x in params['range'].split()]
        n = int(params['n'])
        x = np.linspace(rng[0], rng[1], n)
        np.append(x, coords[:,0])
        x.sort()
        line_colect.append(ax.scatter(coords[:,0], coords[:,1], c='r', s=20))

        y, (p, e) = func(coords, x)
        line_colect.append(ax.plot(x, y, "b--"))
        plugins.connect(fig, plugins.InteractiveLegendPlugin(line_colect,
            ["Точки", "Функция интерполяции"]))
        
        return fig, f"Коэффициенты полинома: $${p}$$RMSE: $${e}$$График:"
    return wrapper

def rmse(a, a_):
    return m.sqrt(sum((a - a_)**2)/a.size)

@result
def lagran(coords, x):
    def lagran_func(coords):
        data_x, data_y = coords[:,0], coords[:,1]
        parameters=[]
        n = len(data_x)
        for i in range(n):
            temp = 1
            for j in range(n):
                if i != j:
                    temp *= data_x[i] - data_x[j]
            parameters.append(data_y[i]/temp)
        
        def interp_func(x):
            nonlocal parameters, data_x
            res = 0
            n = len(parameters)
            for i in range(n):
                temp = 1
                for j in range(n):
                    if i != j:
                        temp *= x - data_x[j]
                res += temp * parameters[i]
            return res
        return interp_func, parameters

    f, p = lagran_func(coords)

    err = rmse(coords[:,1], f(coords[:,0]))
    return f(x), (p, err)


@result
def neuton(coords, x):
    def neuton_func(coords):
        x_data, y_data = coords[:,0], coords[:,1]
        m = len(x_data)
        n = m - 1  # Degree of polynomial
        x_ = np.copy(x_data)
        a = np.copy(y_data)
        for k in range(1, m):
            a[k:m] = (a[k:m] - a[k - 1])/(x_[k:m] - x_[k - 1])
        
        def P(x):
            nonlocal a, x_data
            p = a[n]
            for k in range(1, n + 1):
                p = a[n - k] + (x - x_data[n - k])*p
            return p
        return P, a

    f, p = neuton_func(coords)

    err = rmse(coords[:,1], f(coords[:,0]))

    return f(x), (p.tolist(), err)

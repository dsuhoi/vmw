from numbers import Rational
import networkx as nx
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def result(func):
    def wrapper(params):
        matrix = sp.Matrix([[sp.Rational(x) for x in row.split()] 
        for row in params['matrix'].split('\r\n')])
        result = func(matrix)
        return array_to_LaTeX(np.array(matrix), result)
    return wrapper

def array_to_LaTeX(arr, text):
    arr = arr.astype("str")
    nrow = arr.shape[0]
    rows = [" & ".join(arr[i,:].tolist()) for i in range(nrow)]
    return "\\begin{bmatrix} " + " \\\\ ".join(rows) + " \\end{bmatrix} $$=$$" + text

@result
def determ(a):
    text = sp.latex(sp.Rational(str(a.det())))
    return '$$'+ text + '$$'

@result
def inv(a):
    return a**(-1)

@result
def eigenval(a):
    return a.eigenvals()

@result
def eigenvec(a):
    return a.eigenvects()
import networkx as nx
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def result(func):
    def wrapper(params):
        matrix = sp.Matrix([[sp.Rational(x) for x in row.split()] 
        for row in params['matrix'].split('\r\n')])
        result, text = func(matrix)
        return text + sp.latex(matrix) + '=' + result +'$$'
    return wrapper


@result
def determ(a):
    return sp.latex(sp.Rational(a.det())), '$$det'

@result
def inv(a):
    return sp.latex(a**(-1)), '$$inv'

@result
def eigenval(a):
    return sp.latex(a.eigenvals()), '$$eigenvalues'

@result
def eigenvec(a):
    return sp.latex(a.eigenvects()), '$$eigenvectors'
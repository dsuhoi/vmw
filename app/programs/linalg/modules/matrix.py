import sympy as sp
from app.programs.utils import register_algorithms


def result(func):
    def wrapper(params):
        if str(params["matrix"]).count("\r\n") > 0:
            matrix, oper = parse_operations(params)
        else:
            matrix, oper = parse_one(params)

        result, text = func(*oper, **matrix)
        return "$$" + text + result + "$$"

    register_algorithms(result, func, wrapper)
    return wrapper


def parse_operations(params):
    lst = params["matrix"].split(params["matrix"].split("\r\n")[-1])[0].split("\r\n")
    lst.pop(-1)
    matrix = {}
    for i in lst:
        t = i.split("{", maxsplit=1)[1].replace("{", "").replace("}", "").split(",")
        b = []
        for j in t:
            b.append([sp.Rational(x) for x in j.split()])
        matrix[i.split("{")[0]] = sp.Matrix(b)
    oper = list(str(sp.expand(params["matrix"].split("\r\n")[-1])).replace(" ", ""))
    return matrix, oper


def parse_one(params):
    matrix = {}
    t = (
        params["matrix"]
        .split("{", maxsplit=1)[1]
        .replace("{", "")
        .replace("}", "")
        .split(",")
    )
    b = []
    for i in t:
        b.append([sp.Rational(x) for x in i.split()])
    matrix[params["matrix"].split("{")[0]] = sp.Matrix(b)
    return matrix, ""


@result
def determ(*oper, **matrix):
    keys = list(matrix.keys())
    return (
        sp.latex(sp.Rational(matrix[keys[0]].det())),
        "det" + sp.latex(matrix[keys[0]]) + "=",
    )


@result
def inv(*oper, **matrix):
    keys = list(matrix.keys())
    return sp.latex(matrix[keys[0]] ** (-1)), "inv" + sp.latex(matrix[keys[0]]) + "="


@result
def eigenval(*oper, **matrix):
    keys = list(matrix.keys())
    return (
        sp.latex(matrix[keys[0]].eigenvals()),
        "eigenvalues" + sp.latex(matrix[keys[0]]) + "=",
    )


@result
def eigenvec(*oper, **matrix):
    keys = list(matrix.keys())
    return (
        sp.latex(matrix[keys[0]].eigenvects()),
        "eigenvectors" + sp.latex(matrix[keys[0]]) + "=",
    )


@result
def operations(*oper, **matrix):
    result = ""
    text = ""
    for i in range(len(oper)):
        if i % 2 == 0:
            result += str(matrix[oper[i]])
            text += oper[i]
        else:
            result += oper[i]
            text += oper[i]
    return sp.latex(sp.parse_expr(result)), sp.latex(text + "=")

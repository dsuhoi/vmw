import numpy as np
import sympy as sp
from app.programs.utils import register_algorithms


def result(func):
    def wrapper(params):
        vector_list = np.array(
            [
                [sp.Rational(x) for x in row.split()]
                for row in params["matrix"].split("\r\n")
            ]
        )
        result, text = func(*vector_list)
        return "$$" + text + "=" + result + "$$"

    register_algorithms(result, func, wrapper)
    return wrapper


@result
def mod(*vector_list):
    return sp.latex(np.linalg.norm(vector_list), sp.latex(f"{vector_list}"))


@result
def sum(*vector_list):
    return sp.latex(np.array(vector_list[0]) + np.array(vector_list[1])), sp.latex(
        f"{vector_list[0]}+{vector_list[1]}"
    )


@result
def dif(*vector_list):
    return sp.latex(np.array(vector_list[0]) - np.array(vector_list[1])), sp.latex(
        f"{vector_list[0]}-{vector_list[1]}"
    )


@result
def scalmult(*vector_list):
    return sp.latex(np.vdot(vector_list[0], vector_list[1])), sp.latex(
        f"{vector_list[0]}*{vector_list[1]}"
    )


@result
def vecmult(*vector_list):
    return sp.latex(np.cross(vector_list[0], vector_list[1])), sp.latex(
        f"{vector_list[0]}x{vector_list[1]}"
    )


@result
def mixmult(*vector_list):
    return sp.latex(
        np.vdot(vector_list[0], np.cross(vector_list[1], vector_list[2]))
    ), sp.latex(f"({vector_list[0]},{vector_list[1]},{vector_list[2]})")

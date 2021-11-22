from sympy import latex
from sympy.parsing.sympy_parser import (
    stringify_expr, eval_expr, implicit_multiplication,
    standard_transformations, function_exponentiation, 
    implicit_application, NAME, convert_xor, split_symbols
)

PREEXEC = """from __future__ import division
from sympy import *
import sympy
from sympy.solvers.diophantine import diophantine
"""

SYNONYMS = {
    u'упрощение': 'simplify',
    u'derivative': 'diff',
    u'derive': 'diff',
    u'integral': 'integrate',
    u'antiderivative': 'integrate',
    u'factorize': 'factor',
    u'graph': 'plot',
    u'draw': 'plot'
}

def custom_implicit_transformation(result, local_dict, global_dict):
    for step in (split_symbols, implicit_multiplication,
                 implicit_application, function_exponentiation):
        result = step(result, local_dict, global_dict)
    return result

def synonyms(tokens, local_dict, global_dict):
    result = []
    for token in tokens:
        if token[0] == NAME:
            if token[1] in SYNONYMS:
                result.append((NAME, SYNONYMS[token[1]]))
                continue
        result.append(token)
    return result


def vmw_eval(s):
    namespace = {}
    exec(PREEXEC, {}, namespace)

    transformations = []
    transformations.append(synonyms)
    transformations.extend(standard_transformations)
    transformations.extend((convert_xor, custom_implicit_transformation))
    parsed = stringify_expr(s, {}, namespace, transformations)
    evaluated = eval_expr(parsed, {}, namespace)
    return "$$" + latex(evaluated) + "$$"


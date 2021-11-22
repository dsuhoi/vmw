import sympy as sp


def result(func):
    def wrapper(params):

        lst = params['sets'].replace('},{','|').replace('{','').replace('}','').split('|')
        sets = []
        for l in lst:
            sets.append((sp.FiniteSet(*l.split(','))))
        
        result = func(*sets)
        return "$$" + result + "$$"
    return wrapper

@result
def Union(*sets):
    return sp.latex(sp.Union(*sets))
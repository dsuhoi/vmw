import sympy as sp


def result(func):
    def wrapper(params):
        lst = (
            str(params["sets"])
            .split(str(str(params["sets"]).split("\r\n")[-1]))[0]
            .replace("\r\n", "")
            .split("}")
        )
        lst.pop(-1)
        sets = {}
        for i in lst:
            sets[i.split("{")[0]] = sp.FiniteSet(*i.split("{")[1].split(","))
        oper = list(str(sp.expand(params["sets"].split("\r\n")[-1])).replace(" ", ""))

        result, text = func(*oper, **sets)
        return "$$" + text + "=" + result + "$$"

    return wrapper


@result
def sets_solve(*oper, **sets):
    text = ""
    for i in range(len(oper)):
        if i % 2 == 0:
            text += str(sets[oper[i]])
        else:
            text += oper[i]
    return sp.latex(sp.parse_expr(text)), sp.latex(text)

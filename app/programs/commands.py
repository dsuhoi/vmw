from sympy import latex
from sympy.parsing.sympy_parser import (
    stringify_expr, eval_expr, implicit_multiplication,
    standard_transformations, function_exponentiation, 
    implicit_application, NAME, convert_xor, split_symbols
)
import sympy
import collections
import sys
import ast

PREEXEC = """from __future__ import division
from sympy import *
import sympy
from sympy.solvers.diophantine import diophantine
"""

OTHER_SYMPY_FUNCTIONS = ('sqrt',)

Arguments = collections.namedtuple('Arguments', 'function args kwargs')

SYNONYMS = {
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


class Eval(object):
    def __init__(self, namespace={}):
        self._namespace = namespace

    def get(self, name):
        return self._namespace.get(name)

    def set(self, name, value):
        self._namespace[name] = value

    def eval_node(self, node):
        tree = ast.fix_missing_locations(ast.Expression(node))
        return eval(compile(tree, '<string>', 'eval'), self._namespace)

    def eval(self, x, use_none_for_exceptions=False, repr_expression=True):
        globals = self._namespace
        try:
            x = x.strip()
            x = x.replace("\r", "")
            y = x.split('\n')
            if len(y) == 0:
                return ''
            s = '\n'.join(y[:-1]) + '\n'
            t = y[-1]
            try:
                z = compile(t + '\n', '', 'eval')
            except SyntaxError:
                s += '\n' + t
                z = None

            try:
                old_stdout = sys.stdout
                sys.stdout = StringIO()
                eval(compile(s, '', 'exec', division.compiler_flag), globals, globals)

                if not z is None:
                    r = eval(z, globals)

                    if repr_expression:
                        r = repr(r)
                else:
                    r = ''

                if repr_expression:
                    sys.stdout.seek(0)
                    r = sys.stdout.read() + r
            finally:
                sys.stdout = old_stdout
            return r
        except:
            if use_none_for_exceptions:
                return
            etype, value, tb = sys.exc_info()
            return ""


class LatexVisitor(ast.NodeVisitor):
    EXCEPTIONS = {'integrate': sympy.Integral, 'diff': sympy.Derivative}
    formatters = {}

    @staticmethod
    def formats_function(name):
        def _formats_function(f):
            LatexVisitor.formatters[name] = f
            return f
        return _formats_function

    def format(self, name, node):
        formatter = LatexVisitor.formatters.get(name)

        if not formatter:
            return None

        return formatter(node, self)

    def visit_Call(self, node):
        buffer = []
        fname = node.func.id

        # Only apply to lowercase names (i.e. functions, not classes)
        if fname in self.__class__.EXCEPTIONS:
            node.func.id = self.__class__.EXCEPTIONS[fname].__name__
            self.latex = sympy.latex(self.evaluator.eval_node(node))
        else:
            result = self.format(fname, node)
            if result:
                self.latex = result
            elif fname[0].islower() and fname not in OTHER_SYMPY_FUNCTIONS:
                buffer.append("\\mathrm{%s}" % fname.replace('_', '\\_'))
                buffer.append('(')

                latexes = []
                for arg in node.args:
                    if isinstance(arg, ast.Call) and getattr(arg.func, 'id', None) and arg.func.id[0].lower() == arg.func.id[0]:
                        latexes.append(self.visit_Call(arg))
                    else:
                        latexes.append(sympy.latex(self.evaluator.eval_node(arg)))

                buffer.append(', '.join(latexes))
                buffer.append(')')

                self.latex = ''.join(buffer)
            else:
                self.latex = sympy.latex(self.evaluator.eval_node(node))
        return self.latex


def latexify(string, evaluator):
    a = LatexVisitor()
    a.evaluator = evaluator
    a.visit(ast.parse(string))
    return a.latex


def vmw_eval(s):
    namespace = {}
    exec(PREEXEC, {}, namespace)
    evaluator = Eval(namespace) 
    transformations = []
    transformations.append(synonyms)
    transformations.extend(standard_transformations)
    transformations.extend((convert_xor, custom_implicit_transformation))
    parsed = stringify_expr(s, {}, namespace, transformations)
    evaluated = eval_expr(parsed, {}, namespace)
    
    result = {'input': latexify(parsed, evaluator), 'output': latex(evaluated)}

    return result

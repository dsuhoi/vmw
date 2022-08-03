from flask import render_template, request

from . import programs
from .commands import sympy_eval


@programs.route("/")
def index():
    result = None
    try:
        answer = request.args.get("answer")
        if answer and answer != "":
            result = {}
            result = sympy_eval(answer)
    except Exception as e:
        return render_template("programs.html", answer=answer, error=e.__str__())
    else:
        return render_template("programs.html", answer=answer, result=result)

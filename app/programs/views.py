from flask import Flask, request, render_template, redirect, url_for
from . import programs
from .commands import vmw_eval
@programs.route('/')
def index():
    result = None
    try:
        answer = request.args.get('answer')
        if answer and answer!='':
            result = {}
            result = vmw_eval(answer)
    except Exception as e:
        return render_template('programs.html', answer=answer, error=e.__str__())
    else:
        return render_template('programs.html', answer=answer, result=result)


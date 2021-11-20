from . import linalg as lng
from app.programs.utils import render_decorator
from flask import request, render_template

@lng.route('/')
def index():
    return render_template('linalg.html')

@lng.route('matrix', methods=['GET'])
def matrix():
    @render_decorator('matrix.html', ['matrix'])
    def function(task, params, config):
        text = ''
        return text
    return function()
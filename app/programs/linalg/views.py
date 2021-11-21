from . import linalg as lng
from app.programs.utils import render_decorator
from flask import request, render_template
# import mpld3
from .modules import matrix as matrix_module

@lng.route('/')
def index():
    return render_template('linalg.html')

@lng.route('/matrix', methods=['GET'])
def matrix():
    @render_decorator('matrix.html', ['matrix'])
    def function(task, params, config):
        global g_result_html
        # config['iframe'] = True
        text = None
        if task=='determ':
            text = matrix_module.determ(params)
        elif task=='inv':
            text = matrix_module.inv(params)
        elif task=='eigenval':
            text = matrix_module.eigenval(params)
        elif task=='eigenvec':
            text = matrix_module.eigenvec(params)
        # g_result_html = mpld3.fig_to_html(figure)
        return text
    return function()
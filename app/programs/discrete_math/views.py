from . import discrete_math as dscm
from app.programs.utils import render_decorator
from flask import request, render_template
import mpld3
from .modules import graph as graph_module

# График для генерации
g_result_html = None

@dscm.route('/result')
def result():
    global g_result_html
    return g_result_html

@dscm.route('/')
def index():
    return render_template('linalg.html')

@dscm.route('/graphs', methods=['GET'])
def graphs():
    @render_decorator('graphs.html', ['matrix'])
    def function(task, params, config):
        global g_result_html
        config['iframe'] = True
        text = None
        if task=='create':
            figure, text = graph_module.create(params)
        elif task=='planar':
            figure, text = graph_module.planar(params)
        elif task=='chromatic':
            figure, text = graph_module.chromatic(params)
        g_result_html = mpld3.fig_to_html(figure)
        return text
    return function()

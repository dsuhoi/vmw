from . import discrete_math as dscm
from app.programs.utils import render_decorator
from flask import request, render_template
from .modules import graph as graph_module
from .modules import sets as sets_module



@dscm.route('/')
def index():
    return render_template('linalg.html')

@dscm.route('/graphs', methods=['GET'])
def graphs():
    @render_decorator('graphs.html', ['matrix'])
    def function(task, params, config):
        if task=='create':
            graphJSON, text = graph_module.create(params)
        elif task=='planar':
            graphJSON, text = graph_module.planar(params)
        elif task=='chromatic':
            graphJSON, text = graph_module.chromatic(params)
        elif task=='dijkstra':
            graphJSON,text = graph_module.dijkstra(params)
        config['iframe'] = True
        config['graphJSON'] = graphJSON
        return text
    return function()


@dscm.route('/sets', methods=['GET'])
def sets():
    @render_decorator('sets.html', ['sets'])
    def function(task, params, config):
        text = sets_module.sets_solve(params)
        return text
    return function()

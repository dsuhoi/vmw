from . import discrete_math as dscm
from flask import Flask, request, render_template, redirect, url_for
import mpld3
from .modules import graph

# График для генерации
g_result_html = None

def get_result(volume, task, **params):
    figure = None
    text = None
    if volume=='graph':
        if task=='create':
            figure, text = graph.create(params['matrix'])
        elif task=='planar':
            figure, text = graph.planar(params['matrix'])
        elif task=='chromatic':
            figure, text = graph.chromatic(params['matrix'])
    elif volume=='bulean':
        if task:
            pass
    return mpld3.fig_to_html(figure), text

@dscm.route('/')
def index():
    return render_template('discrete_math.html')

@dscm.route('/graphs', methods=['GET'])
def graphs():
    global g_result_html
    result = None
    try:
        matrix = ""
        matrix_get = request.args.get('matrix')
        task_get = request.args.get('task_list')
        params = {'matrix': matrix_get}
        if matrix_get and matrix_get !='':
            result = {}
            matrix = [[int(x) for x in row.split()] 
                    for row in matrix_get.split('\r\n')]
            g_result_html, result['text']  = get_result('graph', task_get, matrix=matrix)
        else:
            params['matrix'] = ""
    except Exception as e:
        return render_template('graphs.html', params=params, error=e.__str__())
    else:
        return render_template('graphs.html', params=params,
                result=result)

@dscm.route('/result')
def result():
    global g_result_html
    result = g_result_html
    g_result_html = None
    return result


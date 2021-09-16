from . import comp_math as compm
from .modules import deriv as der
from .modules import nae as nae_module
from flask import Flask, request, render_template, redirect, url_for
import mpld3


# График для генерации
g_result_html = None

@compm.route('/result')
def result():
    global g_result_html
    return g_result_html

def get_result(volume, task, params):
    figure = None
    text = None
    if volume=='deriv':
        figure, text = der.derivative(params)
    return mpld3.fig_to_html(figure), text

@compm.route('/')
def index():
    return render_template('comp_math.html')

@compm.route('/deriv', methods=['GET'])
def deriv():
    global g_result_html
    result = None
    try:
        params = {}
        for arg in ('function', 'ranges', 'n', 'd0'):
            params[arg] = request.args.get(arg)
        if params['function'] and params['function']!='':
            result = {}
            g_result_html, result['text'] = get_result('deriv', '', params)
    except Exception as e:
        return render_template('deriv.html', params=params, error=e.__str__())
    else:
        return render_template('deriv.html', params=params, result=result)

@compm.route('/nae', methods=['GET'])
def nae():
    result = None
    try:
        params = {}
        task_get = request.args.get('task_list')
        for arg in ('function', 'range', 'e'):
            params[arg] = request.args.get(arg)
        if params['function'] and params['function']!='':
            result = {'no_iframe': True}
            if task_get == 'half_del':
                result['text'] = nae_module.half_del(params)
            elif task_get == 'simple_iter':
                result['text'] = nae_module.simple_iter(params)
                pass
    except Exception as e:
        raise e
        return render_template('nae.html', params=params, error=e.__str__())
    else:
        return render_template('nae.html', params=params, result=result)


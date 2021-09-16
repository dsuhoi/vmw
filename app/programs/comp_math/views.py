from . import comp_math as compm
from .modules.deriv import derivative
from flask import Flask, request, render_template, redirect, url_for
import mpld3


# График для генерации
g_result_html = None

def get_result(volume, task, params):
    figure = None
    text = None
    if volume=='deriv':
        figure, text = derivative(params)
    elif volume=='1':
        if task=='':
            pass
        elif task=='':
            pass
        elif task=='':
            pass
    elif volume=='':
        if task:
            pass
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

@compm.route('/result')
def result():
    global g_result_html
    return g_result_html


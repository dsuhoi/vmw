from . import comp_math as compm
from .modules import deriv as der
from .modules import nae as nae_module
from .modules import snae as snae_module
from .modules import interp as interp_module
from .modules import diff as diff_module
from .modules import optimize as opt_module
from app.programs.utils import render_decorator
from flask import request, render_template
import mpld3


# График для генерации
g_result_html = None

@compm.route('/result')
def result():
    global g_result_html
    return mpld3.fig_to_html(g_result_html)

@compm.route('/')
def index():
    return render_template('comp_math.html')


@compm.route('/deriv', methods=['GET'])
def deriv():
    @render_decorator('deriv.html', ['function', 'ranges', 'n', 'd0'])
    def function(task, params, config):
        global g_result_html
        config['iframe'] = True
        g_result_html, result = der.derivative(params)
        return result
    return function()


@compm.route('/nae', methods=['GET'])
def nae():
    @render_decorator('nae.html', ['function', 'range', 'e'])
    def function(task, params, config):
        if task == 'half_del':
            result = nae_module.half_del(params)
        elif task == 'simple_iter':
            result = nae_module.simple_iter(params)
        return result
    return function()

@compm.route('/snae', methods=['GET'])
def snae():
    @render_decorator('snae.html', ['functions', 'd0', 'e'])
    def function(task, params, config):
        result = snae_module.gaus_zeid(params)
        return result
    return function()


@compm.route('/interp', methods=['GET'])
def interp():
    @render_decorator('interp.html', ['coords', 'range', 'n'])
    def function(task, params, config):
        global g_result_html
        config['iframe'] = True
        if task == 'lagran':
            g_result_html, result = interp_module.lagran(params)
        elif task == 'neuton':
            g_result_html, result = interp_module.neuton(params)
        return result
    return function()

@compm.route('/diff', methods=['GET'])
def diff():
    @render_decorator('diff.html', ['function', 'd0', 'dx', 'coord'])
    def function(task, params, config):
        global g_result_html
        config['iframe'] = True
        if task == 'mod_euler':
            g_result_html, result = diff_module.mod_euler(params)
        elif task == 'euler_koshi':
            g_result_html, result = diff_module.euler_koshi(params)
        return result
    return function()


@compm.route('/optimize', methods=['GET'])
def optimize():
    @render_decorator('optimize.html', ['function', 'd0', 'dx', 'e'])
    def function(task, params, config):
        result = None
        if task == 'gaus_zeid':
            result = opt_module.gaus_zeid(params)
        elif task == 'relax':
            result = opt_module.relax(params)
        return result
    return function()

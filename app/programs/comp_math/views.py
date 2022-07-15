from app.programs.utils import render_decorator
from flask import render_template

from . import comp_math as compm
from .modules import deriv as der
from .modules import diff as diff_module
from .modules import interp as interp_module
from .modules import nae as nae_module
from .modules import optimize as opt_module
from .modules import snae as snae_module


@compm.route("/")
def index():
    return render_template("comp_math.html")


@compm.route("/deriv", methods=["GET"])
@render_decorator(["function", "ranges", "n", "d0"])
def deriv(task, params, config):
    graphJSON, result = der.derivative(params)
    config["graphJSON"] = graphJSON
    config["iframe"] = True
    return result


@compm.route("/nae", methods=["GET"])
@render_decorator(["function", "range", "e"])
def nae(task, params, config):
    if task == "half_det":
        result = nae_module.half_det(params)
    elif task == "simple_iter":
        result = nae_module.simple_iter(params)
    return result


@compm.route("/snae", methods=["GET"])
@render_decorator(["functions", "d0", "e"])
def snae(task, params, config):
    result = snae_module.gaus_zeid(params)
    return result


@compm.route("/interp", methods=["GET"])
@render_decorator(["coords", "range", "n"])
def interp(task, params, config):
    if task == "lagran":
        graphJSON, result = interp_module.lagran(params)
    elif task == "neuton":
        graphJSON, result = interp_module.neuton(params)
    config["iframe"] = True
    config["graphJSON"] = graphJSON
    return result


@compm.route("/diff", methods=["GET"])
@render_decorator(["function", "d0", "dx", "coord"])
def diff(task, params, config):
    if task == "euler":
        result = diff_module.euler(params)
    elif task == "mod_euler":
        result = diff_module.mod_euler(params)
    elif task == "euler_koshi":
        result = diff_module.euler_koshi(params)
    elif task == "runge_kutt":
        result = diff_module.runge_kutt(params)
    return result


@compm.route("/optimize", methods=["GET"])
@render_decorator(["function", "d0", "dx", "e"])
def optimize(task, params, config):
    result = None
    if task == "gaus_zeid":
        result = opt_module.gaus_zeid(params)
    elif task == "relax":
        result = opt_module.relax(params)
    return result

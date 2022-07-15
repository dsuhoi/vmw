from app.programs.utils import get_algorithms, render_decorator
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
    return get_algorithms(der.result, params, config)


@compm.route("/nae", methods=["GET"])
@render_decorator(["function", "range", "e"])
def nae(task, params, config):
    return get_algorithms(nae_module.result, params, config, task)


@compm.route("/snae", methods=["GET"])
@render_decorator(["functions", "d0", "e"])
def snae(task, params, config):
    return get_algorithms(snae_module.result, params, config)


@compm.route("/interp", methods=["GET"])
@render_decorator(["coords", "range", "n"])
def interp(task, params, config):
    return get_algorithms(interp_module.result, params, config, task)


@compm.route("/diff", methods=["GET"])
@render_decorator(["function", "d0", "dx", "coord"])
def diff(task, params, config):
    return get_algorithms(diff_module.result, params, config, task)


@compm.route("/optimize", methods=["GET"])
@render_decorator(["function", "d0", "dx", "e"])
def optimize(task, params, config):
    return get_algorithms(opt_module.result, params, config, task)

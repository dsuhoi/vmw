from app.programs.utils import get_algorithms, render_decorator
from flask import render_template

from . import discrete_math as dscm
from .modules import graph as graph_module
from .modules import sets as sets_module


@dscm.route("/")
def index():
    return render_template("linalg.html")


@dscm.route("/graphs", methods=["GET"])
@render_decorator(["matrix"])
def graphs(task, params, config):
    return get_algorithms(graph_module.result, params, config, task)


@dscm.route("/sets", methods=["GET"])
@render_decorator(["sets"])
def sets(task, params, config):
    return get_algorithms(sets_module.result, params, config)

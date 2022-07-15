from app.programs.utils import render_decorator
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
    if task == "create":
        graphJSON, text = graph_module.create(params)
    elif task == "planar":
        graphJSON, text = graph_module.planar(params)
    elif task == "chromatic":
        graphJSON, text = graph_module.chromatic(params)
    elif task == "dijkstra":
        graphJSON, text = graph_module.dijkstra(params)
    config["iframe"] = True
    config["graphJSON"] = graphJSON
    return text


@dscm.route("/sets", methods=["GET"])
@render_decorator(["sets"])
def sets(task, params, config):
    text = sets_module.sets_solve(params)
    return text

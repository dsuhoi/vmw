from app.programs.utils import render_decorator
from flask import render_template

from . import linalg as lng
from .modules import matrix as matrix_module
from .modules import vectors as vectors_module


@lng.route("/")
def index():
    return render_template("linalg.html")


@lng.route("/matrix", methods=["GET"])
@render_decorator(["matrix"])
def matrix(task, params, config):
    text = None
    if task == "determ":
        text = matrix_module.determ(params)
    elif task == "inv":
        text = matrix_module.inv(params)
    elif task == "eigenval":
        text = matrix_module.eigenval(params)
    elif task == "eigenvec":
        text = matrix_module.eigenvec(params)
    elif task == "operations":
        text = matrix_module.operation(params)
    return text


@lng.route("/vectors", methods=["GET"])
@render_decorator(["matrix"])
def vectors(task, params, config):
    text = None
    if task == "mod":
        text = vectors_module.mod(params)
    elif task == "sum":
        text = vectors_module.sum(params)
    elif task == "dif":
        text = vectors_module.dif(params)
    elif task == "scalmult":
        text = vectors_module.scalmult(params)
    elif task == "vecmult":
        text = vectors_module.vecmult(params)
    elif task == "mixmult":
        text = vectors_module.mixmult(params)
    return text

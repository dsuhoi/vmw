from app.programs.utils import get_algorithms, render_decorator
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
    return get_algorithms(matrix_module.result, params, config, task)


@lng.route("/vectors", methods=["GET"])
@render_decorator(["matrix"])
def vectors(task, params, config):
    return get_algorithms(vectors_module.result, params, config, task)

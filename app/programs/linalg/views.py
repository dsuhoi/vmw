from app.programs.utils import get_routes_for_module
from flask import render_template

from . import linalg as lng
from .modules import matrix, vectors


@lng.route("/")
def index():
    return render_template("linalg.html")


get_routes_for_module(lng, [matrix, vectors])

from app.programs.utils import get_routes_for_module
from flask import render_template

from . import comp_math as compm
from .modules import deriv, diff, interp, nae, optimize, snae


@compm.route("/")
def index():
    return render_template("comp_math.html")


get_routes_for_module(compm, [deriv, diff, interp, nae, optimize, snae])

from app.programs.utils import get_routes_for_module
from flask import render_template

from . import discrete_math as dscm
from .modules import graphs, sets


@dscm.route("/")
def index():
    return render_template("linalg.html")


get_routes_for_module(dscm, [graphs, sets])

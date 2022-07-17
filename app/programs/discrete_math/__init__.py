from flask import Blueprint

discrete_math = Blueprint(
    "discrete_math", __name__, template_folder="templates", url_prefix="/discrete_math"
)

from . import views

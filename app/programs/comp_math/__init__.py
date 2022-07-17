from flask import Blueprint

comp_math = Blueprint(
    "comp_math", __name__, template_folder="templates", url_prefix="/comp_math"
)

from . import views

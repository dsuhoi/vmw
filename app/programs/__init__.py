from flask import Blueprint
from .comp_math import comp_math
from .discrete_math import discrete_math

programs = Blueprint('programs', __name__, url_prefix='/programs')
programs.register_blueprint(comp_math)
programs.register_blueprint(discrete_math)


from . import views

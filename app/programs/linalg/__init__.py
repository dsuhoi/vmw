from flask import Blueprint

linalg = Blueprint('linalg', __name__,
        template_folder='templates', url_prefix='/linalg')

from . import views

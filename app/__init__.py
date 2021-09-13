import os
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    from .main import main as main_blueprint
    from .programs import programs as programs_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(programs_blueprint, url_prefix='/programs')

    return app

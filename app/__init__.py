from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from .admin import create_admin
from .main import main as main_blueprint
from .programs import programs as programs_blueprint

db = SQLAlchemy()


def create_app(config_env):
    app = Flask(__name__)
    app.config.from_object(config_env)

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(programs_blueprint, url_prefix='/programs')
    
    # set optional bootswatch theme
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name="ВМП", template_mode="bootstrap4")

    return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_basicauth import BasicAuth

db = SQLAlchemy()
migrate = Migrate()
basic_auth = BasicAuth()

def create_app(config_env):
    app = Flask(__name__)
    app.config.from_object(config_env)
    
    db.init_app(app)
    migrate.init_app(app, db)
    basic_auth.init_app(app)

    from .main import main as main_blueprint
    from .programs import programs as programs_blueprint

    app.register_blueprint(main_blueprint, url_prefix='/')
    app.register_blueprint(programs_blueprint, url_prefix='/programs')

    from .admin import create_admin
    admin = create_admin(app)

    return app

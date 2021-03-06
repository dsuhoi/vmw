from flask import Flask
from flask_basicauth import BasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
basic_auth = BasicAuth()


def create_app(config_env):
    app = Flask(__name__)
    app.config.from_object(config_env or "config")

    db.init_app(app)
    migrate.init_app(app, db)
    basic_auth.init_app(app)

    from .main import main as main_blueprint
    from .post import post as post_blueprint
    from .programs import programs as programs_blueprint

    app.register_blueprint(main_blueprint, url_prefix="/")
    app.register_blueprint(programs_blueprint, url_prefix="/programs")
    app.register_blueprint(post_blueprint, url_prefix="/post")

    from .admin import create_admin

    admin = create_admin(app)

    return app

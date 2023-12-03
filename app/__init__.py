import os
from flask import Flask
from app.config import config
from app.models import db, migrate
from app.routes import cors, jwt, main
from app.schemas import ma


def create_app(test_mode=False):
    """ Create flask application instance """
    app = Flask(__name__, template_folder='templates')
    if test_mode:
        app.config.from_object(config["test"])
    else:
        env = os.environ.get("FLASK_ENV")
        app.config.from_object(config[env])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    app.register_blueprint(main)
    ma.init_app(app)

    return app

import os

from flask import Flask

from . import db

def create_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'db.sqlite'),
    )
    os.makedirs(app.instance_path, mode=0o750, exist_ok=True)
    if config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(config)

    db.init_app(app)

    return app

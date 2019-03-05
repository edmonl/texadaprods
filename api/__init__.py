import os

from flask import Flask

from . import db, locations, products

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
    app.register_blueprint(products.blueprint, url_prefix='/products')
    app.register_blueprint(locations.blueprint, url_prefix='/locations')

    @app.after_request
    def json_content_type(res):
        res.headers.set('Content-Type', 'application/json')
        return res

    return app

import os
from flask import Flask
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="aZA89Ws!R",
        DATABASE=os.path.join(app.instance_path, "IB.sqlite"),
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    cache.init_app(app)
    app.cache = cache

    @app.route("/Hello")
    def forward():
        return "This Website Exists!"

    app.debug = True

    from . import db
    db.init_app(app)  # flask --app OffbeatStore init-db

    from OffbeatStore.routes import authentication, main, profile, product

    app.register_blueprint(authentication.bp, url_prefix='/authentication')
    app.register_blueprint(main.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(product.bp)

    return app


if __name__ == '__main__':
    create_app()

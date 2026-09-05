from flask import Flask
from .database import init_app, init_db


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE="financeiro.db",
    )

    if test_config:
        app.config.update(test_config)

    init_app(app)

    from .routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        init_db()

    return app

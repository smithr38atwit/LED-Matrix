from flask import Flask

from .views import views


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    app.register_blueprint(views)

    return app

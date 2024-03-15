from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    from app.routes import main_blueprint

    app.register_blueprint(main_blueprint)

    from app.errors import error_pages

    app.register_blueprint(error_pages)

    return app

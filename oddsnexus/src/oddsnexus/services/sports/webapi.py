from flask import Flask

from oddsnexus.services.sports.endpoints import matches_blueprint


def create_app():
    app = Flask(__name__)
    app.register_blueprint(matches_blueprint)
    return app

from flask import Flask

from oddsnexus.services.sports import cache
from oddsnexus.services.sports.endpoints import matches_blueprint


def create_app():
    app = Flask(__name__)
    cache.init_app(app, config={'CACHE_TYPE': 'SimpleCache'})
    
    app.register_blueprint(matches_blueprint)
    return app

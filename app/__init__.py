from flask import Flask
# from .api import api
from app.api import api


blueprints=[(api,'/api')]


def create_app():
    app=Flask(__name__)
    init_blueprint(app, blueprints)
    
    return app


def init_blueprint(app,blueprint):
    for item in blueprint:
        app.register_blueprint(item[0],url_prefix=item[1])
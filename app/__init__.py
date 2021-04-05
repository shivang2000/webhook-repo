from flask import Flask
from flask_pymongo import PyMongo

from app.webhook.routes import webhook, ui, databaseapi
from .extensions import mongo

# Creating our flask app
def create_app():

    app = Flask(__name__)



    # registering all the blueprints
    app.register_blueprint(webhook)
    app.register_blueprint(ui)
    app.register_blueprint(databaseapi)
    
    return app

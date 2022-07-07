import re
from flask import Flask
from flask_restx import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from config import DevConfig
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()


def create_app(config=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    api = Api(app, doc='/docs')
    db.init_app(app)
    migrate.init_app(app, db, render_as_batch=True)
    JWTManager(app)
    CORS(app)

    from auth import auth
    api.add_namespace(auth)
    from recipe import recipe
    api.add_namespace(recipe)

    @app.shell_context_processor
    def make_shell_context():
        return{
            'db':db,
            'reciepe': Recipe,
            'user': User,
        }
    
    return app


from models import Recipe, User
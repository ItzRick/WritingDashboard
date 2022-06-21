from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_caching import Cache
from app.extensions import jwt
from language_tool_python import LanguageTool



# Database instance:
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()
languageToolEn = LanguageTool('en-US')


def create_app(config_class=Config):
    app = Flask(__name__)
    # Prevent CORS errors, make sure we can retrieve things from the react front-end without errors:
    CORS(app, origins=['https://localhost:3000'], expose_headers=["custom-filename"])
    # Retrieve stuff from the config file:
    app.config.from_object(config_class)
    # Start the database:
    db.init_app(app)
    migrate.init_app(app, db)

    cache.init_app(app)
    
    jwt.init_app(app)

    from app.fileapi import bp as fileapi_bp
    app.register_blueprint(fileapi_bp, url_prefix='/fileapi')

    from app.feedback import bp as feedback_bp
    app.register_blueprint(feedback_bp, url_prefix='/feedback')

    from app.projectapi import bp as projectapi_db
    app.register_blueprint(projectapi_db, url_prefix='/projectapi')

    from app.loginapi import bp as loginapi_db
    app.register_blueprint(loginapi_db, url_prefix='/loginapi')

    from app.scoreapi import bp as scoreapi_bp
    app.register_blueprint(scoreapi_bp, url_prefix='/scoreapi')

    from app.clickapi import bp as clickapi_bp
    app.register_blueprint(clickapi_bp, url_prefix='/clickapi')

    # Return the app:
    return app


from app import models

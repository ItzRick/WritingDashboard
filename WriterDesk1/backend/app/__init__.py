from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import jwt

# Database instance:
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    # Prevent CORS errors, make sure we can retrieve things from the react front-end without errors:
    CORS(app, origins=['https://localhost:3000'])
    # Retrieve stuff from the config file:
    app.config.from_object(config_class)
    # Start the database:
    db.init_app(app)
    migrate.init_app(app, db)

    jwt.init_app(app)

    from app.fileapi import bp as fileapi_bp
    app.register_blueprint(fileapi_bp, url_prefix='/fileapi')

    from app.feedback import bp as feedback_bp
    app.register_blueprint(feedback_bp, url_prefix='/feedback')

    from app.loginapi import bp as loginapi_db
    app.register_blueprint(loginapi_db, url_prefix='/loginapi')

    from app.convertToPDF import bp as convertToPDF_db
    app.register_blueprint(convertToPDF_db, url_prefix='/converttopdf')

    # Return the app:
    return app


from app import models

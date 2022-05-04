from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
# Prevent CORS errors, make sure we can retrieve things from the react front-end without errors:
CORS(app, origins=['http://localhost:3000'])
# Retrieve stuff from the config file:
app.config.from_object(Config)
# Start the database:
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

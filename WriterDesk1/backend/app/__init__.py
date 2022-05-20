from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=['http://localhost:3000'])
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.convertToPDF import bp as convertToPDF_db
app.register_blueprint(convertToPDF_db, url_prefix='/converttopdf')

from app import routes, models
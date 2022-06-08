from flask import Blueprint

bp = Blueprint("convertToPDF", __name__)

from app.convertToPDF import routes
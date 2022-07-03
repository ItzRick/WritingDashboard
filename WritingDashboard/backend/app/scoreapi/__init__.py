from flask import Blueprint

bp = Blueprint('scoreapi', __name__)

from app.scoreapi import routes
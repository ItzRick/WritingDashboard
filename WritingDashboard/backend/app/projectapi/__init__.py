from flask import Blueprint

bp = Blueprint('projectapi', __name__)

from app.projectapi import routes
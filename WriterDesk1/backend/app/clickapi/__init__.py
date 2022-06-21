from flask import Blueprint

bp = Blueprint('clickapi', __name__)

from app.clickapi import routes
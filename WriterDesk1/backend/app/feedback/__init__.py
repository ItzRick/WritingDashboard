from flask import Blueprint

bp = Blueprint('feedback', __name__)

from app.fileapi import routes
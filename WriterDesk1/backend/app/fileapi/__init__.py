from flask import Blueprint

bp = Blueprint('fileupload', __name__)

from app.fileapi import routes
from flask import Blueprint

bp = Blueprint('userapi', __name__)

from app.usersapi import routes
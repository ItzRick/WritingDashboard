from flask import Blueprint

bp = Blueprint('loginapi', __name__)

from app.loginapi import routes
import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set the upload folder:
    if not os.path.isdir(os.path.join(basedir, "saved_documents")):
        os.mkdir(os.path.join(basedir, "saved_documents"))
    UPLOAD_FOLDER = os.path.join(basedir, "saved_documents")
    #authentication
    JWT_SECRET_KEY = "super-secret"  # TODO CHANGE SECRET KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

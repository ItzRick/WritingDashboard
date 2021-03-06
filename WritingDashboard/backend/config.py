import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    FEEDBACKVERSION = str(0.01)

    # Set the upload folder:
    if not os.path.isdir(os.path.join(basedir, "saved_documents")):
        os.mkdir(os.path.join(basedir, "saved_documents"))
    UPLOAD_FOLDER = os.path.join(basedir, "saved_documents")
    #authentication
    JWT_SECRET_KEY = "super-secret"  # TODO CHANGE SECRET KEY
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=4)
    PASSWORD_LENGTH = 10  # Length of generated passwords for participants

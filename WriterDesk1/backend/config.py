import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Set the upload folder:
    if not os.path.isdir(os.path.join(basedir, "saved_documents")):
        os.mkdir(os.path.join(basedir, "saved_documents"))
    UPLOAD_FOLDER = os.path.join(basedir, "saved_documents")

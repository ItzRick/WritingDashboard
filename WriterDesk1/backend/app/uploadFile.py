from distutils.command.upload import upload
from werkzeug.utils import secure_filename
from app import app
import os
from app.models import Files
from app import db
from app.database import uploadToDatabase

def fileUpload(files):
    for file in files:
        # Check if we have received the correct file:
        filename = secure_filename(file.filename)
        # Path to save the file to:
        file_location = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        # print(file_location)
        # Save the file to this path:
        file.save(file_location)
        # Add it to the database:
        addFileToDatabase(filename, file_location)
        print(Files.query.filter_by(filename=filename).first().filename)
        print("done")

def addFileToDatabase(filename, file_location):
    databaseInstance = Files(path=file_location, filename=filename)
    uploadToDatabase(databaseInstance)

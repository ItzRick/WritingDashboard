import os
from werkzeug.utils import secure_filename
from flask import current_app, request
from app.models import Files
from app.fileapi import bp
# from app import db
from app.database import uploadToDatabase

@bp.route('/upload', methods = ['POST'])
def fileUpload():
    # Retrieve the files as send by the react frontend and give this to the fileUpload function, 
    # which does all the work:
    files = request.files.getlist('files')
    # Handle each file separately:
    for file in files:
        print(file)
        # Check if we have received the correct file:
        filename = secure_filename(file.filename)
        # Path to save the file to:
        file_location = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        # print(file_location)
        # Save the file to this path:
        file.save(file_location)
        # Add it to the database:
        fileInDatabase = Files(path=file_location, filename=filename)
        uploadToDatabase(fileInDatabase)
        print(Files.query.filter_by(filename=filename).first().filename)
        print("done")

    return 'success'

import os
from werkzeug.utils import secure_filename
from flask import current_app, request
from app.models import Files
from app.fileapi import bp
# from app import db
from app.database import uploadToDatabase
import magic
from app.exceptions import InvalidUsage

@bp.route('/upload', methods = ['POST'])
def fileUpload():
    # Retrieve the files as send by the react frontend and give this to the fileUpload function, 
    # which does all the work:
    files = request.files.getlist('files')
    data = request.form
    # Handle each file separately:
    for file in files:
        try:
            fileType = magic.from_buffer(file.read(), mime = True)
            isPdf = (fileType == 'application/pdf')
            isDocx = (fileType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            isDoc = (fileType == 'application/msword')
            isTxt = (fileType == 'text/plain')

            if (not (isPdf or isDoc or isDocx or isTxt)):
                raise InvalidUsage('Incorrect file type!')
        except InvalidUsage:
            return 'No correct filetype', 400

        # Check if we have received the correct file:
        filename = secure_filename(file.filename)
        print(filename)
        # Path to save the file to:
        file_location = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        # print(file_location)
        # Save the file to this path:
        file.save(file_location)
        print(file_location)
        # Add it to the database:
        fileInDatabase = Files(path=file_location, filename=filename)
        uploadToDatabase(fileInDatabase)
        print(Files.query.filter_by(filename=filename).first().filename)
        print("done")
    if (len(files) == 0):
        return 'No file uploaded', 400
    return 'success'
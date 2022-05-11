import os
from werkzeug.utils import secure_filename
from flask import current_app, request, session, jsonify
from app.models import Files
from app.fileapi import bp
# from app import db
from app.database import uploadToDatabase, getFilesByUser
import magic
from app.exceptions import InvalidUsage
from datetime import datetime

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

@bp.route('/fileretrieve', methods = ['GET'])
def fileRetrieve():
    # Retrieve list of files that were uploaded by the current user,
    # ordered by the sorting attribute in the request
    if 'user_id' in session or True:
        sortingAttribute = request.args.get('sortingAttribute')
        #TODO change session["user_id"] to actual reference to user
        files = getFilesByUser(0, sortingAttribute)
        
        # Put dates in format
        for file in files:
            file['date'] = file.get('date').strftime('%d/%m/%y %H:%M')
        # Return list of Files objects as json
        return jsonify(files)
    else:
        return 'No user available', 400
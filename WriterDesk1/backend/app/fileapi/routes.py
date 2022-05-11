import os
from werkzeug.utils import secure_filename
from flask import current_app, request, session, jsonify
from app.models import Files
from app.fileapi import bp
# from app import db
from app.database import uploadToDatabase, getFilesByUser
from magic import from_buffer 
from app.exceptions import InvalidUsage
from datetime import date

@bp.route('/upload', methods = ['POST'])
def fileUpload():
    # Retrieve the files as send by the react frontend and give this to the fileUpload function, 
    # which does all the work:
    files = request.files.getlist('files')
    if (len(files) == 0):
        return 'No file uploaded', 400
    fileNames = request.form.getlist('fileName')
    courseCodes = request.form.getlist('courseCode')
    userIds = request.form.getlist('userId')
    dates = request.form.getlist('date')
    # print(fileNames)
    # Handle each file separately:
    for idx, file in enumerate(files):
        try:
            fileType = from_buffer(file.read(), mime = True)
            isPdf = (fileType == 'application/pdf')
            isDocx = (fileType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
            isDoc = (fileType == 'application/msword')
            isTxt = (fileType == 'text/plain')

            if (not (isPdf or isDoc or isDocx or isTxt)):
                raise InvalidUsage('Incorrect file type!')
        except InvalidUsage:
            return 'Incorrect filetype ' + str(idx + 1), 400

        # print(fileNames)
        # Check if we have received the correct file:
        filename = secure_filename(file.filename)
        print(filename)
        # Path to save the file to:
        # fileLocation = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        userFileLocation = os.path.join(current_app.config['UPLOAD_FOLDER'], userIds[idx])
        fileLocation = os.path.join(userFileLocation, filename)
        if not os.path.exists(userFileLocation):
            os.makedirs(userFileLocation)
        if os.path.isfile(fileLocation):
            os.remove(fileLocation)
        # print(file_location)
        # Save the file to this path:
        file.stream.seek(0)
        file.save(fileLocation)
        print(fileLocation)
        date1 = date.fromisoformat(dates[idx])
        # Add it to the database:
        fileInDatabase = Files(path=fileLocation, filename=filename, userId=userIds[idx], courseCode=courseCodes[idx], date=date1)
        uploadToDatabase(fileInDatabase)
        print(Files.query.filter_by(filename=filename).first().filename)
        print("done")
    return 'success'

@bp.route('/fileretrieve', methods = ['GET'])
def fileRetrieve():
    # Retrieve list of files that were uploaded by the current user,
    # ordered by the sorting attribute in the request
    if 'user_id' in session:
        sortingAttribute = request.args.get('sortingAttribute')
        #TODO change session["user_id"] to actual reference to user
        files = getFilesByUser(session['user_id'], sortingAttribute)
        return jsonify(files)
    else:
        return 'No user available', 400
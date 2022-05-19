import os
from werkzeug.utils import secure_filename
from flask import current_app, request, session, jsonify
from app.models import Files
from app.fileapi import bp
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from magic import from_buffer 
from datetime import date

@bp.route('/upload', methods = ['POST'])
def fileUpload():
    '''
        This functions handles the file upload, so handles adding the file to the correct subdirectory
        in the disk of the server and handles adding the required information to the database. So, it handles
        adding the filename, path, courseCode, userId, date to the datebase.
        Attributes:
            files: files as given in the post request by the frontend.
            courseCodes: courseCodes, as given in the post request by the frontend.
            userIds: userIds, of the user uploading each file, as given in the post request by the frontend.
            dates: dates of the files which were uploaded, as given in the post request by the frontend. 
            idx: index of each file that is handled separately.
            file: file, separate instance of each file when it is handled separately.
            fileType: filetype of each specific type that is handled, as read by magic from the header data.
            fileName: the secured filename, of each file that is handled separately, by using secure_filename of flask.
            userFileLocation: the location where the files associated to the current user id should be stored.
            fileLocation: the location where the file that is currently being handled should be stored.
            date1: date of the current file that is being handled in the correct python format. 
            fileInDatabase: information about the current file that is being handled, that should be added to the database. 
            existing: current existing files with the same userId and fileName 
            associated in the database for the current file that is being handled.
    '''
    # Retrieve the files as send by the react frontend and give this to the fileUpload function, 
    # which does all the work:
    files = request.files.getlist('files')
    # If the length of the files, as retrieved is 0, no file has been uploaded, indicate with an error message
    # and a 400 return code:
    if (len(files) == 0):
        return 'No file uploaded', 400
    # Get the other data as sent by the react frontend:
    courseCodes = request.form.getlist('courseCode')
    userIds = request.form.getlist('userId')
    dates = request.form.getlist('date')
    # Handle each file separately:
    for idx, file in enumerate(files):
        # Get the filetype and check if this is one of the accepted filetypes:
        fileType = from_buffer(file.read(), mime = True)
        isPdf = (fileType == 'application/pdf')
        isDocx = (fileType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        isDoc = (fileType == 'application/msword')
        isTxt = (fileType == 'text/plain')

        # If the filetype is not accepted, indicate this by returning this in a message and a 400 code:
        if (not (isPdf or isDoc or isDocx or isTxt)):
            return 'Incorrect filetype ' + str(idx + 1), 400
        # Run secure_filename on the file to protect against sql_injections etc and to make sure the filename does not
        # contain any spaces:
        filename = secure_filename(file.filename)
        # Get the path to save the file to, as indicated in the config and then having a subfolder for every user:
        userFileLocation = os.path.join(current_app.config['UPLOAD_FOLDER'], userIds[idx])
        fileLocation = os.path.join(userFileLocation, filename)
        # If this subdirectory does not exist yet, create it:
        if not os.path.exists(userFileLocation):
            os.makedirs(userFileLocation)
        # If a file with this filename has already been uploaded, remove it:
        if os.path.isfile(fileLocation):
            os.remove(fileLocation)
        # Save the file to this path:
        file.stream.seek(0)
        file.save(fileLocation)
        # Put the date in the correct object, by getting it from the isoformat as given by the frontend:
        date1 = date.fromisoformat(dates[idx])
        # Add it to the database:
        fileInDatabase = Files(path=fileLocation, filename=filename, userId=userIds[idx], courseCode=courseCodes[idx], date=date1)
        # If it already exists in the database for this user and filename, remove it:
        existing = Files.query.filter_by(userId=userIds[idx], filename=filename).all()
        for file in existing:
            removeFromDatabase(file)
        # Add the data to the database:
        uploadToDatabase(fileInDatabase)
    # Indicate that we have successfully uploaded this file to the server:
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
            
        # Return http response with list as json in response body
        return jsonify(files)
    else:
        return 'No user available', 400

@bp.route('/filedelete', methods = ['GET', 'DELETE'])
def fileDelete(): 
    # Delete the file specified, which can be either with id or file name
    if 'file_id' in session: 
        fileToDelete = request.args.get('file_id')
        removeFromDatabase(fileToDelete)
        return 'success'
    else: 
        return 'No file available', 400
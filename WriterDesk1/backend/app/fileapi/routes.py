import os
from werkzeug.utils import secure_filename
from flask import current_app, request, session, jsonify, send_file
from app.models import Files, User, Projects
from app.fileapi import bp
from app.fileapi.convert import convertDocx, convertTxt, removeConvertedFiles
from app.database import uploadToDatabase, getFilesByUser, removeFromDatabase
from magic import from_buffer
from datetime import date
from mimetypes import guess_extension

# jwt
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required

@bp.route('/upload', methods = ['POST'])
@jwt_required()
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
            fileIds: ids of the file that have been uploaded.
            extensionFilename: The extension as retrieved from the fileName.
    '''
    # Retrieve the files as send by the react frontend and give this to the fileUpload function,
    # which does all the work:
    files = request.files.getlist('files')
    fileIds = []
    # If the length of the files, as retrieved is 0, no file has been uploaded, indicate with an error message
    # and a 400 return code:
    if (len(files) == 0):
        return 'No file uploaded', 400
    # Get the other data as sent by the react frontend:
    courseCodes = request.form.getlist('courseCode')
    userId = current_user.id
    dates = request.form.getlist('date')
    # Handle each file separately:
    for idx, file in enumerate(files):
        # Run secure_filename on the file to protect against sql_injections etc and to make sure the filename does not
        # contain any spaces:
        filename = secure_filename(file.filename)
        # Get the filetype and check if this is one of the accepted filetypes:
        fileType = from_buffer(file.read(), mime = True)
        isPdf = (fileType == 'application/pdf')
        isDocx = (fileType == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        isTxt = (fileType == 'text/plain')
        extension = guess_extension(fileType)
        # Get the extension from the filename:
        extensionFilename = filename.split('.')[-1]
        # If the file is corrupt, that is the filename extension is not the actual extension:
        if extension[1:] != extensionFilename:
            return 'Corrupt file: ' + str(filename), 400
        # If the filetype is not accepted, indicate this by returning this in a message and a 400 code:
        if (not (isPdf or isDocx or isTxt)):
            return 'Incorrect filetype: ' + str(filename), 400
        # Get the path to save the file to, as indicated in the config and then having a subfolder for every user:
        userFileLocation = os.path.join(current_app.config['UPLOAD_FOLDER'], str(userId))
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
        fileInDatabase = Files(path=fileLocation, filename=filename, userId=userId, courseCode=courseCodes[idx], date=date1, fileType=extension)
        # If it already exists in the database for this user and filename, remove it:
        existing = Files.query.filter_by(userId=userId, filename=filename).all()
        for file in existing:
            removeFromDatabase(file)
        # Add the data to the database:
        uploadToDatabase(fileInDatabase)
        fileIds.append(fileInDatabase.id)
    # Indicate that we have successfully uploaded this file to the server:
    return f'Uploaded file with ids: {fileIds}'

@bp.route('/fileretrieve', methods = ['GET'])
@jwt_required()
def fileRetrieve():
    '''
    This function handles the retrieval of files in a specified order from a 
    specific user in the form of a json file. 
    This is done by identifying the user and retrieving the preferred sorting. 
    Attributes: 
        userId: user id as given by the frontend
        sortingAttribute: chosen sorting of files as given by the frontend
    Arguments:
        files: the files of the user corresponding to the user id, 
               which are sorted based on the sortingAttribute
        file: one of the files of the list files
    returns:
        On success:
            list of files of the userId
        On error:
            403: if not either userId is current_user or user is current_user is researcher or admin
            403: user is a researcher or admin, but wants to retrieve participants that are not his
    '''
    # Retrieve list of files that were uploaded by the current user,
    # ordered by the sorting attribute in the request

    # get userid
    userId = int(request.args.get('userId'))

    # check if the userId is of current_user
    if current_user.id != userId:
        # or current_user is a researcher or admin
        if (current_user.role != 'researcher' and current_user.role != 'admin'):
            return 'You must be researcher or admin, or retrieve your own data', 403
        # now, some researcher or admin tries to access other userFiles, check if this is its participant

        #ParticipantToProject.query.filter_by(userId=userId).first()
        if User.query.filter_by(id=userId).filter(User.participants.has(userId=current_user.id)).first() is None:
            return 'You can only retrieve data from your participants or yourself', 403
    sortingAttribute = request.args.get('sortingAttribute')
    files = getFilesByUser(userId, sortingAttribute)

    # Put dates in format
    for file in files:
        file['date'] = file.get('date').strftime('%d/%m/%y')

    # Return http response with list as json in response body
    return jsonify(files)

@bp.route('/filedelete', methods = ['DELETE'])
@jwt_required()
def fileDelete():
    '''
    This function handles the deletion of files using the corresponding file id. 
    Attributes: 
        fileID: file id as given by the frontend
    Arguments: 
        fileToBeRemoved: file that is to be removed, using the given file id
        path: path of the file that is to be removed
        basepath: basepath of the path of the file to be removed
    Return:
        response, 200: an http response with the csv file when it was
            created succesfully.
        error 403: if the user accessing this method does not have the
            rights to call it.
        error 404: if file doesn't exists
    '''
    # Get the data as sent by the react frontend:
    fileIDs = request.form.getlist('id')
    for fileID in fileIDs:
        fileToBeRemoved = Files.query.filter_by(id=fileID).first()
        # Check if the file is nonexistent
        # And if so, throw an error message 
        if fileToBeRemoved is None:
            return 'file does not exist in database', 404
        # check if user is authorized to delete file        
        if fileToBeRemoved.userId != current_user.id:
            return 'Unauthorized', 403
        # Retrieve the paths of the file to be removed
        path = fileToBeRemoved.path
        fileType = fileToBeRemoved.fileType
        basepath = os.path.dirname(path)
        # If the path exists, remove the file from the database
        # Else, throw an error message
        if os.path.isfile(path):
            os.remove(path)
            removeConvertedFiles(path, fileType)
            removeFromDatabase(fileToBeRemoved)
            if not os.listdir(basepath):
                os.rmdir(basepath)
        else:
            return 'file does not exist', 404
    # Return a success message when done
    return 'succes', 200


@bp.route('/searchId', methods = ['GET'])
def searchId():
    '''
    This function handles making a list of the file ids, 
    such that it can be used later to search for a file. 
    Attributes: 
        files: contains all the files on the database at the time of creation
    Arguments:
        list: contains the string of each file id with spaces afterwards
        file: one of the list files
    '''
    files = Files.query.all()
    list = ""
    for file in files:
        list += (str(file.id) + ' ')
    return list, 200


@bp.route('/getFileById', methods = ['GET'])
@jwt_required()
def getFileById():
    '''
    This function handles the retrieval of a single file by the fileId.
    Attributes:
        fileId: File id as given by the frontend.
    Arguments:
        file: File of the user corresponding to the file id.
        filedict: Dictionary containing all the attributes of a file.
    '''
    # Get the data as sent by the react frontend
    fileId = request.args.get('fileId')

    # Check if the fileId exists in Files
    if Files.query.filter_by(id=fileId).first() is None:
        return 'No file found with fileId', 400

    # Query the correct file
    file = Files.query.filter_by(id=fileId).first()

    # Create dictionary for the correct file
    filedict = {
        "id": file.id,
        "userId": file.userId,
        "path": file.path,
        "filename": file.filename,
        "filetype": file.fileType,
        "courseCode": file.courseCode,
        "date": file.date.strftime('%d/%m/%y')
    }
    return filedict, 200


@bp.route('/display', methods= ['GET'])
@jwt_required()
def displayFile():
    '''
        Function to convert a document of type docx or txt to a document of
        type pdf. And returns this file.
        Attributes:
            filepath: the path to the document to be converted.
            filetype: the type of the document to be converted.
            pdf: used in making a pdf from a txt file.
        Return:
            Take the converted document from the disk and send it.
    '''
    filepath = request.args.get('filepath')
    filetype = request.args.get('filetype')
    # if the document is a docx file, convert using the convertDocx module and return the converted document.
    if filetype == 'docx':
        newPath = convertDocx(filepath)
        return send_file(newPath)
    # if the document is a txt file, convert it to a pdf by making a new pdf using the contents of the txt file,
    # then return the converted document.
    elif filetype == 'txt':
        newPath = convertTxt(filepath)
        return send_file(newPath)
    # The file has not been converted, send the original file.
    return send_file(filepath)

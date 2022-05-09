import os
from werkzeug.utils import secure_filename
from flask import current_app, request, session
from app.models import Files
from app.fileapi import bp
# from app import db
from app.database import uploadToDatabase, getFilesByUser

@bp.route('/upload', methods = ['POST'])
def fileUpload():
    # Retrieve the files as send by the react frontend and give this to the fileUpload function, 
    # which does all the work:
    files = request.files.getlist('files')
    # Handle each file separately:
    for file in files:
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
        return 'failure'
    return 'success'

@bp.route('/fileretrieve', methods = ['GET'])
def fileRetrieve():
    print(request.args.get('sortingAttribute'))
    # Retrieve list of files that were uploaded by the current user
    if "user_id" in session:
        sortingAttribute = request.args.get('sortingAttribute')
        #TODO change session["user_id"] to actual reference to user
        files = database.getFilesByUser(session["user_id"], sortingAttribute)
        return jsonify(files)
    else:
        return "no user"
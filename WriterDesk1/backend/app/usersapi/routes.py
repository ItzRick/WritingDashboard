import os

from flask import jsonify

from app.database import getUsers
from app.models import User
from app.usersapi import bp
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
from flask import request

from app.database import removeFromDatabase
from app.fileapi.routes import fileDelete
from app.models import Files, Explanations, Scores, ParticipantToProject, Projects


@bp.route('/users', methods=['GET'])
@jwt_required()
def usersRetrieve():
    '''
        This function handles the retrieval of users except for users
        with the participant role in the form of a json file.
        Attributes:
            users: list containing all users (each entry has the username, id and role of a user)
            except for participants
        Return:
            Returns json file containing users
    '''

    if current_user.role != 'admin':
        return 'Method only accessible for admin users', 403

    # Retrieve list of files that were uploaded by the current user,
    # ordered by the sorting attribute in the request
    users = getUsers()

    if len(users) != 0:
        # Return http response with list as json in response body
        return jsonify(users)
    else:
        return 'No user available', 400


# Removes the given user and the associated files, explanations and scores from the database
@bp.route('/deleteUser', methods=['POST'])
@jwt_required()
def deleteUser():
    userID = request.json.get("userID", None)
    if userID == '':
        userID = current_user.id
    filesToBeRemoved = Files.query.filter_by(userId=userID).all()
    for i in filesToBeRemoved:
        fileID = i.id
        explanationsToBeRemoved = Explanations.query.filter_by(fileId=fileID).all()
        for j in explanationsToBeRemoved:
            removeFromDatabase(j)
        scoresToBeRemoved = Scores.query.filter_by(fileId=fileID).all()
        for j in scoresToBeRemoved:
            removeFromDatabase(j)
        deleteFile(i)
    participantToProjectToBeRemoved = ParticipantToProject.query.filter_by(userId=userID).all()
    for j in participantToProjectToBeRemoved:
        removeFromDatabase(j)
    projectsToBeRemoved = Projects.query.filter_by(userId=userID).all()
    for j in projectsToBeRemoved:
        removeFromDatabase(j)
    userToBeRemoved = User.query.filter_by(id=userID).first()
    removeFromDatabase(userToBeRemoved)
    return 'Account deleted!', 200


def deleteFile(fileToBeRemoved):
    # Check if the file is nonexistent
    # And if so, throw an error message
    if fileToBeRemoved == None:
        return 'file does not exist in database', 404
    # Retrieve the paths of the file to be removed
    path = fileToBeRemoved.path
    basepath = os.path.dirname(path)
    # If the path exists, remove the file from the database
    # Else, throw an error message
    if os.path.isfile(path):
        os.remove(path)
        removeFromDatabase(fileToBeRemoved)
        if not os.listdir(basepath):
            os.rmdir(basepath)
    else:
        return 'file does not exist', 404
    # Return a success message when done
    return 'succes', 200

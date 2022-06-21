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
            error message:
                403, if the current user is not an admin
    '''

    if current_user.role != 'admin':
        return 'Method only accessible for admin users', 403

    # Retrieve list of files that were uploaded by the current user,
    # ordered by the sorting attribute in the request
    users = getUsers()
    # Return http response with list as json in response body
    return jsonify(users)


@bp.route('/deleteUserAdmin', methods=['POST'])
@jwt_required()
def deleteUserAdmin():
    if current_user.role != 'admin':
        return 'Method only accessible for admin users', 403
    userID = request.json.get("userID", None)
    deleteUser(userID)
    return 'Account deleted!', 200

@bp.route('/deleteUserResearcher', methods=['POST'])
@jwt_required()
def deleteUserResearcher():
    if current_user.role != 'researcher':
        return 'Method only accessible for researcher users', 403
    userID = request.json.get("userID", None)
    user = User.query.filter_by(id=userID)
    if user.role != 'participant':
        return 'Target user is not an participant', 403
    project = ParticipantToProject.query.filter_by(userId=user.id).first()
    for researcherProject in Projects.query.filter_by(userId=current_user.id):
        if project.projectName == researcherProject.projectName:
            deleteUser(userID)
            return 'Account deleted!', 200
    return 'Participant is not created by this researcher', 403


@bp.route('/deleteUserSelf', methods=['POST'])
@jwt_required()
def deleteUserSelf():
    deleteUser(current_user.id)
    return 'Account deleted!', 200


# Removes the given user and the associated files, explanations and scores from the database
def deleteUser(userID):
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

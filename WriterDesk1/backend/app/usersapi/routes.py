import os
from flask import request, jsonify
from app import db

from app.database import getUsers, getParticipantsWithProjectsByResearcher
from app.models import User, Projects, ParticipantToProject
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
    '''
        This function deletes the user corresponding to the userId that is supplied by the front-end.
        The function can only be used when signed in as an user with the admin role.
        Attributes:
            userID: userId supplied by the front-end
        Return:
            Returns a string saying the account is deleted with a 200 code.
            error message:
                403, when calling this function while not singed is as an admin.
                404, when trying to delete an user that does not exist.
    '''
    if current_user.role != 'admin':
        return 'Method only accessible for admin users', 403
    userID = request.json.get("userID", None)
    if User.query.filter_by(id=userID).first() is None:
        return 'User does not exist', 404
    deleteUser(userID)
    return 'Account deleted!', 200


@bp.route('/deleteUserResearcher', methods=['POST'])
@jwt_required()
def deleteUserResearcher():
    '''
        This function deletes the user with the participant role corresponding to the userId that is
        supplied by the front-end.
        The function can only be used when signed in as an user with the admin or researcher role and only allows
        participants belonging to the signed in user's projects to be deleted.
        Attributes:
            userID: userId supplied by the front-end
            user: user corresponding to userID
            project: project the participant to be deleted is in
            projectID: projectId corresponding to project
        Return:
            Returns a string saying the account is deleted with a 200 code.
            error message:
                403, when calling this function while not singed is as an admin or researcher.
                404, when trying to delete an user that does not exist.
                403, when trying to delete an user that is not a participant.
                403, when trying to delete an user that is a participant but does not belong to
                a project owned by the currently singed in user.
    '''
    if current_user.role != 'researcher' and current_user.role != 'admin':
        return 'Method only accessible for researcher and admin users', 403
    userID = request.json.get("userID", None)
    if User.query.filter_by(id=userID).first() is None:
        return 'User does not exist', 404
    user = User.query.filter_by(id=userID).first()
    if user.role != 'participant':
        return 'Target user is not an participant', 403
    projectID = ParticipantToProject.query.filter_by(userId=user.id).first().projectId
    project = Projects.query.filter_by(id=projectID).first()
    # loops over the projects owned by the currently signed in user and checks whether the user to
    # be deleted is related to one of them, if not an error is thrown.
    for researcherProject in Projects.query.filter_by(userId=current_user.id):
        if project.projectName == researcherProject.projectName:
            deleteUser(userID)
            return 'Account deleted!', 200
    return 'Participant is not created by this researcher', 403


@bp.route('/deleteUserSelf', methods=['POST'])
@jwt_required()
def deleteUserSelf():
    '''
        This function deletes the currently signed in user.
        Return:
            Returns a string saying the account is deleted with a 200 code.
    '''
    deleteUser(current_user.id)
    return 'Account deleted!', 200


# Removes the given user and the associated files, explanations and scores from the database
def deleteUser(userID):
    '''
        This function deletes the user corresponding to the supplied userId and through dependencies everything
        that is related to said user.
        Attributes:
            filesToBeRemoved: the files owned by the user
            usersToBeRemoved: the user corresponding to the supplied userId
        Arguments:
            userID: the userId related to the user that needs to be deleted.
    '''
    filesToBeRemoved = Files.query.filter_by(userId=userID).all()
    for i in filesToBeRemoved:
        deleteFile(i)
    userToBeRemoved = User.query.filter_by(id=userID).first()
    removeFromDatabase(userToBeRemoved)


def deleteFile(fileToBeRemoved):
    '''
        This function deletes the supplied file from both the database and the disk.
        Attributes:
            path: path of given file
            basepath: basepath of the to be removed file
        Arguments:
            fileToBeRemoved: the database entry of the to be removed file
        Return:
            returns a string with succes and a 200 code
            error message:
                404, if the file does not exist in the database
                404, if the file does not exist on the disk
    '''
    # Check if the file is nonexistent
    # And if so, throw an error message
    if fileToBeRemoved is None:
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


@bp.route('/getParticipantsProjects', methods=['GET'])
@jwt_required()
def getParticipantsProjects():
    '''
    This function handles retrieving the participants and related for a particular user
    The user must be an admin or researcher to access this method
    TODO: descibe return data
    Attributes:
        researcherId: id of the researcher or admin calling this function
    Return:
        Returns success if it succeeded, or an 
        error message:
            403, if the current_user is neither an admin nor a researcher
    '''
    # check if user is admin OR researcher (i.e. reject if user is neither)
    if current_user.role != 'admin' and current_user.role != 'researcher':
        return 'Method only accessible for admin or researcher users', 403
    

    # get researcher id
    researcherId = current_user.id

    # retrieve researcher data
    data = getParticipantsWithProjectsByResearcher(researcherId)
    # return data
    return jsonify(data), 200

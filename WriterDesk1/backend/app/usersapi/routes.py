from flask import request, jsonify
from app import db

from app.database import getUsers, getParticipantsWithProjectsByResearcher
from app.models import User, Projects, ParticipantToProject
from app.usersapi import bp
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user


@bp.route('/users', methods=['GET'])
@jwt_required()
def usersRetrieve():
    if current_user.role != 'admin':
        return 'Method only accessible for admin users', 403
    '''
    This function handles the retrieval of users except for users
    with the participant role in the form of a json file.
    '''
    # Retrieve list of files that were uploaded by the current user,
    # ordered by the sorting attribute in the request
    users = getUsers()

    if len(users) != 0:
        # Return http response with list as json in response body
        return jsonify(users)
    else:
        return 'No user available', 400

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

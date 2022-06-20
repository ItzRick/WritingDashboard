from app.projectapi import bp

from flask import request, jsonify
from app.models import Projects

from app.database import uploadToDatabase, removeFromDatabase, getProjectsByResearcher, getParticipantsWithProjectsByResearcher
from app import generateParticipants as gp
from app import db

import os
import shutil

from app.projectapi import bp

from flask import request, jsonify, current_app
from app.models import Projects, User, ParticipantToProject

from app.database import uploadToDatabase, removeFromDatabase, getParticipantsByResearcher, getProjectsByResearcher
from app import generateParticipants as gp
from app import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user



@bp.route('/addparticipants', methods=["POST"])
def addParticipantsToExistingProject():
    '''
    This function handles the creation of new participants and adding them to an existing project.
    It raises an error when participants were not added to database.
    Attributes:
        count: the number of participants that should be added
        projectId: the id of the project the participants should be added to
    '''
    # Retrieve data from request
    count = int(request.json.get("count", None))
    projectId = int(request.json.get("projectid", None))

    # Try to register new user in database
    try:
        gp.generateParticipants(count, projectId)
        return "Participants were successfully added!", 200
    except Exception as e:
        return str(e), 400

@bp.route('/setProject', methods=['POST'])
@jwt_required()
def setProject():
    '''
    This function handles the creation of research projects using a user id and a project name.
    Attributes:
        projectName: project name as given by the frontend
        current_user: the user currently logged in
        projectIndb: project object that is uploaded to the database
    '''
    # Get the data as sent by the react frontend:
    projectName = request.form.get('projectName')

    if User.query.filter_by(id=current_user.id).first().role == 'student' \
            or User.query.filter_by(id=current_user.id).first().role == 'participant':
        return 'User is not admin or researcher', 400

    # create Projects object
    projectIndb = Projects(userId=current_user.id, projectName=projectName)

    # Upload row to database
    db.session.add(projectIndb)
    db.session.flush()
    db.session.commit()

    return str(projectIndb.id), 200


@bp.route('/deleteProject', methods=['DELETE'])
@jwt_required()
def deleteProject():
    '''
    This function handles the deletion of research projects using the corresponding project id's. If the project
    does not exist in the database, the function raises a 404 error. If the project has a different user than the current
    user, the function raises a 400 error.
    Attributes:
        projectIds: List of project id's as given by the frontend
        projectToBeRemoved: project object that is going to be removed
    '''
    # Get the data as sent by the react frontend:
    projectIds = request.form.getlist('projectId')

    for projectId in projectIds:
        if Projects.query.filter_by(id=projectId).first() is None:
            return 'project does not exist in database', 404

        # Check if the project that is going to be deleted is related to the current user
        if current_user.id != Projects.query.filter_by(id=projectId).first().userId:
            return 'Project is not related to current user', 400

    DeleteAllFilesFromProject(projectIds)  # Remove all files corresponding to the project ids from the server

    for projectId in projectIds:
        # Retrieve the row that needs to be removed
        projectToBeRemoved = Projects.query.filter_by(id=projectId).first()

        # Remove row from database
        removeFromDatabase(projectToBeRemoved)

    return 'success', 200


def DeleteAllFilesFromProject(projectIds):
    '''
    This function handles the deletion of files corresponding to all users from a project.
    Attributes:
        users: Users corresponding to project removed
        folderToRemove: path of folder that needs to be removed
    Arguments:
        projectIds: List of project id's as given by the frontend
    '''

    for projectId in projectIds:
        # Retrieve users of project with project id
        users = ParticipantToProject.query.filter_by(projectId=projectId).all()
        for user in users:
            try:
                folderToRemove = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user.userId))
                shutil.rmtree(folderToRemove)  # Try to remove folder recursively
            except FileNotFoundError:
                print('Folder not found')
    return 'success', 200

@bp.route('/viewparticipantsofuser', methods=["GET"])
def viewParticipantsOfUser():
    '''
    This function handles the showing the participants that
    this specific user created to that user, using that user id.
    Attributes:
        userId: user id as given by the frontend
    Arguments:
        participants: the participants that this user has created
    '''
    # Get the user id as sent by the react frontend
    userId = request.args.get('userId')
    # Retrieve the information from the participants corresponding to the projects of the user
    participants = getParticipantsWithProjectsByResearcher(userId)
    # Throw an error if the project variable is empty
    # in other words, if the user has no projects
    if participants == []:
        return 'researcher has no participants', 4041
    return jsonify(participants)

@bp.route('/viewprojectsofuser', methods=["GET"])
def viewProjectsOfUser():
    '''
    This function handles the showing the projects that
    this specific user created to that user, using that user id.
    Attributes:
        userId: user id as given by the frontend
    Arguments:
        projects: the projects that this user has created
    '''
    # Get the user id as sent by the react frontend
    userId = request.args.get('userId')

    # Retrieve the information from the projects corresponding to the projects of the user
    projects = getProjectsByResearcher(userId)

    # Throw an error if the project variable is empty
    # in other words, if the user has no projects
    if projects == []:
        return 'researcher has no projects', 4041

    return jsonify(projects)
    
import os
import shutil

from app.projectapi import bp

from flask import request, jsonify, current_app
from app.models import Projects, User, ParticipantToProject

from app.database import removeFromDatabase, getProjectsByResearcher, recordsToCsv, getParticipantsWithProjectsByResearcher
from app import generateParticipants as gp
from app import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

@bp.route('/addParticipants', methods=["POST"])
@jwt_required()
def addParticipantsToExistingProject():
    '''
        This function handles the creation of new participants and adding them to an existing project.
        It raises an error when participants were not added to database.
        Attributes:
            nrOfParticipants: the number of participants that should be added
            projectId: the id of the project the participants should be added to
            data: dictionary with usernames and passwords of new participants
            path: path to csv with usernames and passwords
            response: http response with csv file
        Return:
            Returns an http response with a csv file, a 'Content-Disposition: attachment' header 
            and 'custom-filename' header with a name for the file when participant creation was successful
            and the error if it was not.
    '''
    # Retrieve data from request
    nrOfParticipants = int(request.json.get("nrOfParticipants", None))
    projectId = int(request.json.get("projectid", None))

    # Try to register new user in database
    try:
        data = gp.generateParticipants(nrOfParticipants, projectId)

        # Create csv file
        path = os.path.join(current_app.config['UPLOAD_FOLDER'], str(current_user.id), "downloadParticipants.csv")
        recordsToCsv(path, data)

        # Generator to delete file after sending
        def generate():
            with open(path) as f:
                yield from f

            os.remove(path)

        # Create response
        response = current_app.response_class(generate(), mimetype='text/csv')
        # Set headers to show that the response contains a file and what the name of the file should be
        response.headers.set('Content-Disposition', 'attachment')
        response.headers.set('custom-filename', 'participants.csv')
        return response, 200
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
        Return:
            Returns string with project id if project creation was successful and an error message otherwise.
    '''
    # Get the data as sent by the react frontend:
    projectName = request.form.get('projectName')

    # Check if current user has rights to create a project
    if current_user.role != 'admin' and current_user.role != 'researcher':
        return 'User is not admin or researcher', 400

    # Create Projects object
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
        Return:
            Returns a string with 'success' if project deletion was successful and an error message otherwise.
    '''
    # Get the data as sent by the react frontend:
    projectIds = request.form.getlist('projectId')

    for projectId in projectIds:
        if Projects.query.filter_by(id=projectId).first() is None:
            return 'project does not exist in database', 404

        # Check if the project that is going to be deleted is related to the current user
        if current_user.id != Projects.query.filter_by(id=projectId).first().userId:
            return 'Project is not related to current user', 400

    deleteAllFilesFromProject(projectIds)  # Remove all files corresponding to the project ids from the server

    for projectId in projectIds:
        # Retrieve the row that needs to be removed
        projectToBeRemoved = Projects.query.filter_by(id=projectId).first()

        # Remove row from database
        removeFromDatabase(projectToBeRemoved)

    return 'success', 200


def deleteAllFilesFromProject(projectIds):
    '''
        This function handles the deletion of files corresponding to all users from a project.
        Attributes:
            users: Users corresponding to project removed
            folderToRemove: path of folder that needs to be removed
        Arguments:
            projectIds: List of project id's as given by the frontend
        Return:
            Returns a string with a success message.
    '''

    for projectId in projectIds:
        # Retrieve users of project with project id
        users = ParticipantToProject.query.filter_by(projectId=projectId).all()
        for user in users:
            folderToRemove = os.path.join(current_app.config['UPLOAD_FOLDER'], str(user.userId))
            # If the folder exists:
            if os.path.isdir(folderToRemove):
                shutil.rmtree(folderToRemove)  # Try to remove folder recursively

@bp.route('/viewParticipantsOfUser', methods=["GET"])
def viewParticipantsOfUser():
    '''
    This function handles the showing the participants that
    this specific user created to that user, using that user id.
    Attributes:
        userId: user id as given by the frontend
        participants: the participants that this user has created
    '''
    # Get the user id as sent by the react frontend
    userId = request.args.get('userId')
    # Retrieve the information from the participants corresponding to the projects of the user
    participants = getParticipantsWithProjectsByResearcher(userId)
    # Throw an error if the project variable is empty
    # in other words, if the user has no projects
    if participants == []:
        return 'researcher has no participants', 404
    return jsonify(participants)

@bp.route('/viewProjectsOfUser', methods=["GET"])
@jwt_required()
def viewProjectsOfUser():
    '''
    This function handles the showing the projects of the current user 
    if the current user is an admin or researcher
    Attributes:
        projects: the projects that this user has created
    returns:
        if success, the projectData and the number of participants related to the project
            in an array
        if error:
            403, if the current user is not a researcher or admin
    '''
    if current_user.role != 'researcher' and current_user.role != 'admin':
        return 'Method only accessible for researcher and admin users', 403

    # Retrieve the information from the projects corresponding to the projects of the user
    projects = getProjectsByResearcher(current_user.id)

    return jsonify(projects)
    

from app.projectapi import bp

from flask import request, jsonify
from app.models import Projects, User

from app.database import uploadToDatabase, removeFromDatabase, getParticipantsByResearcher, getProjectsByResearcher
from app import generateParticipants as gp
from app import db
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user



@bp.route('/addparticipants', methods=["POST"])
def addParticipantsToExistingProject():

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
    Arguments:
        projectIndb: project object that is uploaded to the database
    '''
    # Get the data as sent by the react frontend:
    projectName = request.form.get('projectName')

    if User.query.filter_by(id=current_user.id).first() is None:
        return 'user not found', 404

    # create Projects object
    projectIndb = Projects(userId=current_user.id, projectName=projectName)

    # Upload row to database
    db.session.add(projectIndb)
    db.session.flush()
    db.session.commit()

    return str(projectIndb.id), 200


@bp.route('/deleteProject', methods=['DELETE'])
def deleteProject():
    '''
    This function handles the deletion of research projects using the corresponding project id's.
    Attributes:
        projectIds: List of project id's as given by the frontend
    Arguments:
        projectToBeRemoved: project object that is going to be removed
    '''
    # Get the data as sent by the react frontend:
    projectIds = request.form.getlist('projectId')

    for projectId in projectIds:
        # Retrieve the row that needs to be removed
        projectToBeRemoved = Projects.query.filter_by(id=projectId).first()

        if projectToBeRemoved is None:
            return 'project does not exist in database', 404

        # Remove row from database
        removeFromDatabase(projectToBeRemoved)

    return 'success', 200

@bp.route('/viewparticipantsofuser', methods=["GET"])
def viewParticipantsOfUser():
    # Get the user id as sent by the react frontend
    userId = request.args.get('userId')

    # Retrieve the information from the participants corresponding to the projects of the user
    participants = getParticipantsByResearcher(userId)
    if participants is None:
        return 'researcher has no participants', 404

    return jsonify(participants)

@bp.route('/viewprojectsofuser', methods=["GET"])
def viewProjectsOfUser():
    # Get the user id as sent by the react frontend
    userId = request.args.get('userId')

    # Retrieve the information from the projects corresponding to the projects of the user
    projects = getProjectsByResearcher(userId)
    if projects is None:
        return 'researcher has no projects', 404

    return jsonify(projects)
    
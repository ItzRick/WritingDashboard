from app.projectapi import bp

from flask import request, jsonify
from app.models import Projects

from app.database import uploadToDatabase, removeFromDatabase


@bp.route('/setProject', methods=['POST'])
def setProject():
    # Get the data as sent by the react frontend:
    userId = request.form.get('userId')
    projectName = request.form.get('projectName')

    # create Projects object
    projectIndb = Projects(userId=userId, projectName=projectName)

    # upload
    uploadToDatabase(projectIndb)
    return 'successfully created project'


@bp.route('/deleteProject', methods=['DELETE'])
def deleteProject():
    # Get the data as sent by the react frontend:
    projectId = request.form.get('projectId')

    projectToBeRemoved = Projects.query.filter_by(id=projectId).first()

    if projectToBeRemoved is None:
        return 'project does not exist in database', 404

    removeFromDatabase(projectToBeRemoved)
    return 'successfully deleted project'

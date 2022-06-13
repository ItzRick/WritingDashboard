from app.projectapi import bp

from flask import request, jsonify
from app.models import Projects

from app.database import uploadToDatabase, removeFromDatabase


@bp.route('/setProject', methods=['POST'])
def setProject():
    # Get the data as sent by the react frontend:
    userId = request.form.get('userId')
    projectName = request.form.get('projectName')
    userId = 123
    projectName = 'Test'
    return setProjectDB(userId, projectName)


def setProjectDB(userId, projectName):
    # Check if the fileId exists in Files
    if Projects.query.filter_by(userId=userId).first() is None:
        return 'No user found with userId', 400

    # create Projects object
    projectIndb = Projects(id=123, userId=userId, projectName=projectName)
    # upload
    uploadToDatabase(projectIndb)
    return 'successfully created project'

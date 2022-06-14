from flask import request
from app.projectapi import bp
from app import generateParticipants as gp

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
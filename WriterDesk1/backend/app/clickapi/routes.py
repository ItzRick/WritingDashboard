from app.clickapi import bp

from flask import request
from app.models import Clicks, User
from app.database import uploadToDatabase
from flask_jwt_extended import jwt_required, current_user

@bp.route('/setClick', methods = ['POST'])
@jwt_required()
def setClick():
    '''
        set click for the current user, triggered when a user views a document, or clicks an event
        Attributes:
            userId: user id of the currently logged in user
            url: url of the page where the click happened
            eventType: type of event, can be one of [click.button, click.link, view.document, click.highlight]
            actionId: in case of a click: name of the button
                      in case of a view: name of the document
        Return:
            Returns 'successfully uploaded click' if it succeeded, or an 
            error message:
                451, if the current user does not want to get tracked
                400, if the eventType is not one of [click.button, click.link, view.document, click.highlight]

    '''
    # get user id from current user
    userId = current_user.id 
    # get the data as sent by the react frontend:
    url = request.form.get('url', None)
    eventType = request.form.get('eventType', None)
    actionId = request.form.get('actionId', None)

    # check if user wants to be tracked (ignoring trackability for participants)
    if not current_user.trackable and current_user.role != 'participant':
        return 'User clicks not trackable', 451
    # check if eventType is one of [click.button, click.link, view.document]
    if eventType not in ["click.button", "click.link", "view.document", "click.highlight"]:
        return 'Invalid eventType', 400

    # create Clicks object
    clickInDB = Clicks(
        userId=userId,
        url=url,
        eventType=eventType,
        actionId=actionId,
    )
    # upload
    uploadToDatabase(clickInDB)

    return 'successfully uploaded click'

from app.clickapi import bp

from flask import request
from app.models import Clicks, User
from app.database import uploadToDatabase
from flask_jwt_extended import jwt_required, current_user

@bp.route('/setClick', methods = ['POST'])
@jwt_required()
def setClick():
    '''
        set score for the current user
        Attributes:
            userId: user id of the currently logged in user
            url: url of the page where the click happened
            eventType: type of event, can be one of [click.button, click.link, view.document]
            buttonId: id of the button, usually similair to the text displayed on the button, not available for view.document events
            documentId: id of the document being viewed, only availabel for view.document events
            documentName: name of the document being viewed, only availabel for view.document events
        Return:
            Returns 'successfully uploaded click' if it succeeded, or an 
            error message:
                404, if there exists no user with userId
                451, if the current user does not want to get tracked


    '''
    # get user id from current user
    userId = current_user.id 
    # get the data as sent by the react frontend:
    url = request.form.get('url')
    eventType = request.form.get('url')
    buttonId = request.form.get('url')
    documentId = request.form.get('url')
    documentName = request.form.get('url')

    # check if user wants to be tracked (ignoring trackability for participants)
    if not current_user.trackable and current_user.role != 'participant':
        return 'User clicks not trackable', 451

    # create Clicks object
    clickInDB = Clicks(
        userId=userId,
        url=url,
        eventType=eventType,
        buttonId=buttonId,
        documentId=documentId,
        documentName=documentName,
    )
    # upload
    uploadToDatabase(clickInDB)

    return 'successfully uploaded click'
